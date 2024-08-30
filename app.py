from flask import Flask, render_template, request, send_file
import pandas as pd
from scholarly import scholarly
import requests
import io

app = Flask(__name__)

def fetch_publications(author_name, start_year=None, end_year=None):
    try:
        search_query = scholarly.search_author(author_name)
        author = next(search_query)
        scholarly.fill(author, sections=['publications'])
        publications = author['publications']
        
        journals = {}
        conferences = {}
        miscellaneous = []

        for pub in publications:
            pub_info = pub.get('bib', {})
            year = pub_info.get('pub_year', 'Unknown')

            if year == 'Unknown' or not year.isdigit():
                year_label = 'Unknown Year'
                details = {
                    'Title': pub_info.get('title', 'No Title'),
                    'Citation Link': f"https://scholar.google.co.in/citations?view_op=view_citation&hl=en&user={author['scholar_id']}&citation_for_view={pub.get('author_pub_id', 'No Citation ID')}",
                    'Venue': pub_info.get('venue', 'N/A'),
                    'Publisher': pub_info.get('publisher', 'N/A'),
                    'Cited By': pub.get('num_citations', 'N/A'),
                    'Year': year_label
                }
                miscellaneous.append(details)
                continue
            else:
                year_label = int(year)

            title = pub_info.get('title', 'No Title')
            citation_id = pub.get('author_pub_id', 'No Citation ID')
            citation_url = f"https://scholar.google.co.in/citations?view_op=view_citation&hl=en&user={author['scholar_id']}&citation_for_view={citation_id}"

            if start_year is not None and end_year is not None:
                if not (start_year <= year_label <= end_year):
                    continue

            details = {
                'Title': title,
                'Citation Link': citation_url,
                'Venue': pub_info.get('venue', 'N/A'),
                'Publisher': pub_info.get('publisher', 'N/A'),
                'Cited By': pub.get('num_citations', 'N/A'),
                'Year': year_label
            }

            crossref_data = fetch_crossref_details(title)
            details.update(crossref_data)

            journal_or_conference = details.get('journal_or_conference', '').lower()
            if 'conference' in journal_or_conference or 'workshop' in journal_or_conference:
                conferences.setdefault(year_label, []).append(details)
            elif 'journal' in journal_or_conference or 'proceedings' in journal_or_conference:
                journals.setdefault(year_label, []).append(details)
            else:
                miscellaneous.append(details)

        return journals, conferences, miscellaneous
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None

def fetch_crossref_details(title):
    url = f"https://api.crossref.org/works"
    params = {'query.title': title}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get('message', {}).get('items', [])
        if items:
            item = items[0]
            return {
                'journal_or_conference': item.get('container-title', ['N/A'])[0],
                'publisher': item.get('publisher', 'N/A')
            }
    return {'journal_or_conference': 'N/A', 'publisher': 'N/A'}

def save_to_excel(journals, conferences, miscellaneous):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if journals:
            journal_data = []
            for year, papers in sorted(journals.items()):
                for paper in papers:
                    journal_data.append({
                        'Year': year,
                        'Type': 'Journal',
                        'Title': paper['Title'],
                        'Citation Link': paper['Citation Link'],
                        'Venue': paper.get('journal_or_conference', 'N/A'),
                        'Publisher': paper['Publisher'],
                        'Cited By': paper['Cited By']
                    })
            journal_df = pd.DataFrame(journal_data)
            if not journal_df.empty:
                journal_df = journal_df.dropna(axis=1, how='all')
                journal_df.to_excel(writer, sheet_name='Journals', index=False)

        if conferences:
            conference_data = []
            for year, papers in sorted(conferences.items()):
                for paper in papers:
                    conference_data.append({
                        'Year': year,
                        'Type': 'Conference',
                        'Title': paper['Title'],
                        'Citation Link': paper['Citation Link'],
                        'Venue': paper.get('journal_or_conference', 'N/A'),
                        'Publisher': paper['Publisher'],
                        'Cited By': paper['Cited By']
                    })
            conference_df = pd.DataFrame(conference_data)
            if not conference_df.empty:
                conference_df = conference_df.dropna(axis=1, how='all')
                conference_df.to_excel(writer, sheet_name='Conferences', index=False)

        if miscellaneous:
            miscellaneous_df = pd.DataFrame(miscellaneous)
            if not miscellaneous_df.empty:
                miscellaneous_df = miscellaneous_df.dropna(axis=1, how='all')
                miscellaneous_df.to_excel(writer, sheet_name='Miscellaneous', index=False)

    output.seek(0)
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')
        start_year = int(start_year) if start_year and start_year.isdigit() else None
        end_year = int(end_year) if end_year and end_year.isdigit() else None

        journals, conferences, miscellaneous = fetch_publications(author_name, start_year, end_year)

        excel_file = save_to_excel(journals, conferences, miscellaneous)

        return render_template('results.html', 
            journals=journals,
            conferences=conferences,
            miscellaneous=miscellaneous,
            download_url='/download?author_name=' + author_name + '&start_year=' + (str(start_year) if start_year else '') + '&end_year=' + (str(end_year) if end_year else ''),
            author_name=author_name,
            start_year=start_year,
            end_year=end_year)

    return render_template('index.html')

@app.route('/download')
def download():
    author_name = request.args.get('author_name')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    start_year = int(start_year) if start_year and start_year.isdigit() else None
    end_year = int(end_year) if end_year and end_year.isdigit() else None

    journals, conferences, miscellaneous = fetch_publications(author_name, start_year, end_year)
    excel_file = save_to_excel(journals, conferences, miscellaneous)
    
    return send_file(excel_file, as_attachment=True, download_name='publications.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
