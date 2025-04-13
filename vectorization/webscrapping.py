import os
import json
import time
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai

# Load environment variables from the .env file
load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not FIRECRAWL_API_KEY or not GEMINI_API_KEY:
    raise Exception("Please set FIRECRAWL_API_KEY and GEMINI_API_KEY in your .env file.")

# Initialize the Firecrawl app with your API key
app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# (Optional) If needed by the genai library, configure it with your Gemini API key.
# For example, if there is a configuration step, uncomment the line below.
# genai.configure(api_key=GEMINI_API_KEY)

# Select the Gemini model using the genai library.
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_text(text):
    """
    Uses the Gemini model to generate a summary via a text prompt.
    """
    prompt = f"Summarize the following text: {text}"
    response = model.generate_content(prompt)
    return response.text

def scrape_udemy_course(course_url):
    """
    Scrapes a Udemy course page using Firecrawl and summarizes its content using Gemini.
    Returns the summary or an error message.
    """
    try:
        # Request the course page content in markdown format.
        response = app.scrape_url(course_url, params={'formats': ['markdown']})
        course_content = response.get('markdown', '')
        if not course_content:
            return "No content retrieved from the course page."
    except Exception as e:
        return f"Error during scraping: {e}"
    
    # Generate a summary using Gemini.
    summary = summarize_text(course_content)
    return summary

def get_udemy_courses(search_url):
    """
    Scrapes the Udemy search results page and extracts a list of courses.
    Each course is stored as a dictionary with 'title' and 'url' keys.
    """
    try:
        response = app.scrape_url(search_url, params={'formats': ['html']})
        html_content = response.get('html', '')
        if not html_content:
            print("No content retrieved from the search page.")
            return []
    except Exception as e:
        print(f"Error scraping search page: {e}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    courses = []
    
    # Try to find course cards via a known attribute.
    course_cards = soup.find_all('div', attrs={"data-purpose": "search-course-card"})
    if course_cards:
        for card in course_cards:
            title_elem = card.find('h3')
            title = title_elem.get_text(strip=True) if title_elem else "No Title"
            link_elem = card.find('a', href=True)
            course_url = link_elem['href'] if link_elem else ""
            if course_url and course_url.startswith('/'):
                course_url = "https://www.udemy.com" + course_url
            courses.append({"title": title, "url": course_url})
    else:
        # Fallback: search for anchor tags with '/course/' in the href.
        course_links = soup.find_all('a', href=True)
        for link in course_links:
            href = link['href']
            if '/course/' in href:
                title = link.get_text(strip=True)
                if not title:
                    continue
                # Avoid duplicates.
                if any(course['url'] == href or course['title'] == title for course in courses):
                    continue
                if href.startswith('/'):
                    href = "https://www.udemy.com" + href
                courses.append({"title": title, "url": href})
    
    return courses

def main():
    # URL for Udemy search results (DataScience courses)
    search_url = "https://www.udemy.com/courses/search/?src=ukw&q=DataScience"
    courses = get_udemy_courses(search_url)
    print(f"Found {len(courses)} courses.")
    
    # Iterate over each course and generate a summary.
    for idx, course in enumerate(courses, start=1):
        print(f"Processing course {idx}/{len(courses)}: {course['title']}")
        summary = scrape_udemy_course(course["url"])
        course["summary"] = summary
        # Optionally, add a delay to avoid hitting rate limits.
        time.sleep(2)
    
    # Save the course data (including summaries) to a JSON file.
    output_file = "courses_summary2.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)
    print(f"Course summaries saved to {output_file}")

if __name__ == "__main__":
    main()
