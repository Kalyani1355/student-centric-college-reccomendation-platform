import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# =========================================================
# STANDARD COURSE PATTERNS
# =========================================================

COURSE_PATTERNS = {
    "MCA": [
        r"\bmca\b",
        r"\bmaster\s+of\s+computer\s+applications?\b",
    ],
    "BCA": [
        r"\bbca\b",
        r"\bbachelor\s+of\s+computer\s+applications?\b",
    ],
    "MBA": [
        r"\bmba\b",
        r"\bmaster\s+of\s+business\s+administration\b",
    ],
    "BBA": [
        r"\bbba\b",
        r"\bbachelor\s+of\s+business\s+administration\b",
    ],
    "B.Tech": [
        r"\bb\.?\s*tech\b",
        r"\bbachelor\s+of\s+technology\b",
    ],
    "M.Tech": [
        r"\bm\.?\s*tech\b",
        r"\bmaster\s+of\s+technology\b",
    ],
    "B.Sc": [
        r"\bb\.?\s*sc\b",
        r"\bbachelor\s+of\s+science\b",
    ],
    "M.Sc": [
        r"\bm\.?\s*sc\b",
        r"\bmaster\s+of\s+science\b",
    ],
    "B.Com": [
        r"\bb\.?\s*com\b",
        r"\bbachelor\s+of\s+commerce\b",
    ],
    "M.Com": [
        r"\bm\.?\s*com\b",
        r"\bmaster\s+of\s+commerce\b",
    ],
    "B.Pharm": [
        r"\bb\.?\s*pharm\b",
        r"\bbachelor\s+of\s+pharmacy\b",
    ],
    "M.Pharm": [
        r"\bm\.?\s*pharm\b",
        r"\bmaster\s+of\s+pharmacy\b",
    ],
    "B.Arch": [
        r"\bb\.?\s*arch\b",
        r"\bbachelor\s+of\s+architecture\b",
    ],
    "M.Arch": [
        r"\bm\.?\s*arch\b",
        r"\bmaster\s+of\s+architecture\b",
    ],
    "LLB": [
        r"\bllb\b",
        r"\bbachelor\s+of\s+laws?\b",
    ],
    "LLM": [
        r"\bllm\b",
        r"\bmaster\s+of\s+laws?\b",
    ],
    "MBBS": [
        r"\bmbbs\b",
        r"\bbachelor\s+of\s+medicine\b",
    ],
    "BDS": [
        r"\bbds\b",
        r"\bbachelor\s+of\s+dental\s+surgery\b",
    ],
    "B.Ed": [
        r"\bb\.?\s*ed\b",
        r"\bbachelor\s+of\s+education\b",
    ],
    "M.Ed": [
        r"\bm\.?\s*ed\b",
        r"\bmaster\s+of\s+education\b",
    ],
    "PhD": [
        r"\bph\.?\s*d\b",
        r"\bphd\b",
        r"\bdoctor\s+of\s+philosophy\b",
    ],
    "Diploma": [
        r"\bdiploma\b",
    ],
}


# =========================================================
# REQUEST SESSION
# =========================================================

session = requests.Session()

session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
)


# =========================================================
# URL HELPERS
# =========================================================

def normalize_url(url):

    if not url:
        return None

    url = url.strip()

    if not url:
        return None

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def same_domain(url1, url2):

    try:
        domain1 = urlparse(url1).netloc.lower()
        domain2 = urlparse(url2).netloc.lower()

        return domain1 == domain2

    except Exception:
        return False


# =========================================================
# FETCH PAGE
# =========================================================

def get_page(url):

    try:

        response = session.get(
            url,
            timeout=12,
            allow_redirects=True
        )

        if response.status_code != 200:

            print(
                f"FAILED: {url} "
                f"STATUS={response.status_code}"
            )

            return None, None, (
                f"HTTP {response.status_code}"
            )

        content_type = (
            response.headers
            .get("content-type", "")
            .lower()
        )

        if "text/html" not in content_type:

            return (
                response.url,
                None,
                f"Not HTML: {content_type}"
            )

        return (
            response.url,
            response.text,
            ""
        )

    except Exception as error:

        print(
            "FETCH ERROR:",
            url,
            error
        )

        return None, None, str(error)


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# COURSE MATCHING
# =========================================================

def match_courses(text):

    text = clean_text(text)

    if not text:
        return []

    found = []

    for course, patterns in COURSE_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                found.append(course)
                break

    return found


# =========================================================
# IGNORE BAD HTML AREAS
# =========================================================

def is_ignored_element(tag):

    ignored_tags = {
        "script",
        "style",
        "noscript",
        "svg"
    }

    if tag.name in ignored_tags:
        return True

    parent = tag.parent

    while parent:

        if parent.name in {
            "script",
            "style",
            "noscript",
            "svg"
        }:
            return True

        # Don't use navigation/footer content
        # as course evidence.
        if parent.name in {
            "nav",
            "footer"
        }:
            return True

        parent = parent.parent

    return False


# =========================================================
# EVIDENCE SCORE
# =========================================================

def calculate_score(
    tag,
    text,
    source_url
):

    score = 0

    tag_name = (
        tag.name.lower()
        if tag.name
        else ""
    )

    class_text = " ".join(
        tag.get("class", [])
    ).lower()

    id_text = (
        tag.get("id", "")
        or ""
    ).lower()

    context = (
        class_text
        + " "
        + id_text
    )

    # -----------------------------------------------------
    # Strong HTML elements
    # -----------------------------------------------------

    if tag_name in {
        "h1",
        "h2",
        "h3"
    }:
        score += 3

    elif tag_name in {
        "h4",
        "h5",
        "h6"
    }:
        score += 2

    elif tag_name in {
        "td",
        "th"
    }:
        score += 2

    elif tag_name == "li":
        score += 2

    elif tag_name == "a":
        score += 2

    # -----------------------------------------------------
    # Course-related container
    # -----------------------------------------------------

    course_context_words = [
        "course",
        "courses",
        "program",
        "programs",
        "programme",
        "programmes",
        "academic",
        "academics",
        "degree",
        "degrees",
        "department",
        "departments",
        "admission",
        "admissions"
    ]

    if any(
        word in context
        for word in course_context_words
    ):
        score += 3

    # -----------------------------------------------------
    # Strong degree wording
    # -----------------------------------------------------

    strong_phrases = [
        "master of computer applications",
        "bachelor of computer applications",
        "master of business administration",
        "bachelor of business administration",
        "bachelor of technology",
        "master of technology",
        "bachelor of science",
        "master of science",
        "bachelor of commerce",
        "master of commerce",
        "bachelor of pharmacy",
        "master of pharmacy",
        "bachelor of architecture",
        "master of architecture",
        "bachelor of education",
        "master of education",
        "doctor of philosophy"
    ]

    lower_text = text.lower()

    for phrase in strong_phrases:

        if phrase in lower_text:
            score += 3
            break

    # -----------------------------------------------------
    # Course-specific URL
    # -----------------------------------------------------

    lower_url = source_url.lower()

    if any(
        word in lower_url
        for word in [
            "course",
            "program",
            "programme",
            "academic",
            "admission",
            "degree"
        ]
    ):
        score += 2

    # -----------------------------------------------------
    # Very large text = weak evidence
    # -----------------------------------------------------

    if len(text) > 1500:
        score -= 2

    return score


# =========================================================
# CREATE EVIDENCE
# =========================================================

def create_evidence(
    course,
    text,
    source_url,
    tag,
    score
):

    text = clean_text(text)

    if len(text) > 350:
        text = text[:350] + "..."

    return {
        "course": course,
        "source": source_url,
        "text": text,
        "score": score,
        "element": tag.name
        if tag.name
        else ""
    }


# =========================================================
# ANALYZE ONE HTML PAGE
# =========================================================

def analyze_page(
    html,
    page_url
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    detected = set()
    evidence = []

    # Remove only technical HTML
    for tag in soup.find_all(
        [
            "script",
            "style",
            "noscript",
            "svg"
        ]
    ):
        tag.decompose()

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    if soup.title:

        title = clean_text(
            soup.title.get_text(
                " ",
                strip=True
            )
        )

        matches = match_courses(
            title
        )

        for course in matches:

            # Title is useful evidence,
            # but not enough alone.
            score = 2

            evidence.append(
                create_evidence(
                    course,
                    title,
                    page_url,
                    soup.title,
                    score
                )
            )

    # -----------------------------------------------------
    # HEADINGS
    # -----------------------------------------------------

    for tag in soup.find_all(
        [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6"
        ]
    ):

        if is_ignored_element(tag):
            continue

        text = clean_text(
            tag.get_text(
                " ",
                strip=True
            )
        )

        if not text:
            continue

        matches = match_courses(
            text
        )

        if not matches:
            continue

        score = calculate_score(
            tag,
            text,
            page_url
        )

        for course in matches:

            if score >= 3:

                detected.add(course)

                evidence.append(
                    create_evidence(
                        course,
                        text,
                        page_url,
                        tag,
                        score
                    )
                )

    # -----------------------------------------------------
    # TABLE ROWS
    # -----------------------------------------------------

    for tag in soup.find_all("tr"):

        if is_ignored_element(tag):
            continue

        text = clean_text(
            tag.get_text(
                " ",
                strip=True
            )
        )

        if not text or len(text) > 1200:
            continue

        matches = match_courses(
            text
        )

        if not matches:
            continue

        score = calculate_score(
            tag,
            text,
            page_url
        )

        for course in matches:

            if score >= 3:

                detected.add(course)

                evidence.append(
                    create_evidence(
                        course,
                        text,
                        page_url,
                        tag,
                        score
                    )
                )

    # -----------------------------------------------------
    # LIST ITEMS
    # -----------------------------------------------------

    for tag in soup.find_all("li"):

        if is_ignored_element(tag):
            continue

        text = clean_text(
            tag.get_text(
                " ",
                strip=True
            )
        )

        if not text or len(text) > 500:
            continue

        matches = match_courses(
            text
        )

        if not matches:
            continue

        score = calculate_score(
            tag,
            text,
            page_url
        )

        for course in matches:

            if score >= 3:

                detected.add(course)

                evidence.append(
                    create_evidence(
                        course,
                        text,
                        page_url,
                        tag,
                        score
                    )
                )

    # -----------------------------------------------------
    # COURSE-RELATED LINKS
    # -----------------------------------------------------

    course_link_words = [
        "course",
        "courses",
        "program",
        "programs",
        "programme",
        "programmes",
        "academic",
        "academics",
        "degree",
        "admission"
    ]

    for tag in soup.find_all(
        "a",
        href=True
    ):

        if is_ignored_element(tag):
            continue

        text = clean_text(
            tag.get_text(
                " ",
                strip=True
            )
        )

        href = clean_text(
            tag.get(
                "href",
                ""
            )
        )

        if not text:
            continue

        combined = (
            text
            + " "
            + href
        ).lower()

        if not any(
            word in combined
            for word in course_link_words
        ):
            continue

        matches = match_courses(
            text
        )

        if not matches:
            continue

        score = calculate_score(
            tag,
            text,
            page_url
        )

        for course in matches:

            if score >= 3:

                detected.add(course)

                evidence.append(
                    create_evidence(
                        course,
                        text,
                        page_url,
                        tag,
                        score
                    )
                )

    return detected, evidence


# =========================================================
# FIND RELEVANT LINKS
# =========================================================

def find_relevant_links(
    base_url,
    html
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    base_domain = (
        urlparse(
            base_url
        ).netloc.lower()
    )

    keywords = [
        "course",
        "courses",
        "program",
        "programs",
        "programme",
        "programmes",
        "academic",
        "academics",
        "admission",
        "admissions",
        "degree",
        "degrees",
        "department",
        "departments",
        "faculty",
        "faculties",
        "mca",
        "bca",
        "mba",
        "bba",
        "btech",
        "mtech",
        "bsc",
        "msc",
        "bcom",
        "mcom",
        "pharm",
        "arch"
    ]

    links = []

    for anchor in soup.find_all(
        "a",
        href=True
    ):

        href = clean_text(
            anchor.get(
                "href",
                ""
            )
        )

        if not href:
            continue

        if href.startswith(
            (
                "#",
                "javascript:",
                "mailto:",
                "tel:"
            )
        ):
            continue

        full_url = urljoin(
            base_url,
            href
        )

        parsed = urlparse(
            full_url
        )

        if (
            parsed.netloc.lower()
            != base_domain
        ):
            continue

        link_text = clean_text(
            anchor.get_text(
                " ",
                strip=True
            )
        )

        combined = (
            link_text
            + " "
            + href
        ).lower()

        if any(
            word in combined
            for word in keywords
        ):

            links.append(
                full_url
            )

    # Remove duplicate URLs
    unique_links = []

    for link in links:

        if link not in unique_links:
            unique_links.append(link)

    return unique_links[:25]


# =========================================================
# DETAILED SCRAPER
# =========================================================

def scrape_courses_detailed(
    website
):

    website = normalize_url(
        website
    )

    if not website:

        return {
            "success": False,
            "courses": [],
            "evidence": [],
            "pages_checked": 0,
            "errors": [
                "Website not available"
            ]
        }

    print("\n========================================")
    print(
        "SCRAPING:",
        website
    )
    print("========================================")

    all_courses = set()
    all_evidence = []
    errors = []
    pages_checked = 0

    # -----------------------------------------------------
    # MAIN PAGE
    # -----------------------------------------------------

    final_url, html, error = get_page(
        website
    )

    if not html:

        return {
            "success": False,
            "courses": [],
            "evidence": [],
            "pages_checked": 0,
            "errors": [
                error or "Main page failed"
            ]
        }

    main_url = (
        final_url
        or website
    )

    pages_checked += 1

    courses, evidence = analyze_page(
        html,
        main_url
    )

    all_courses.update(
        courses
    )

    all_evidence.extend(
        evidence
    )

    # -----------------------------------------------------
    # INTERNAL COURSE PAGES
    # -----------------------------------------------------

    links = find_relevant_links(
        main_url,
        html
    )

    print(
        "RELEVANT LINKS:",
        len(links)
    )

    for index, link in enumerate(
        links,
        start=1
    ):

        print(
            f"[{index}/{len(links)}]",
            link
        )

        page_url, page_html, page_error = get_page(
            link
        )

        if not page_html:

            if page_error:
                errors.append(
                    {
                        "url": link,
                        "error": page_error
                    }
                )

            continue

        pages_checked += 1

        page_courses, page_evidence = analyze_page(
            page_html,
            page_url or link
        )

        if page_courses:

            print(
                "FOUND:",
                sorted(page_courses)
            )

        all_courses.update(
            page_courses
        )

        all_evidence.extend(
            page_evidence
        )

    # -----------------------------------------------------
    # KEEP BEST EVIDENCE
    # -----------------------------------------------------

    best_evidence = {}

    for item in all_evidence:

        course = item["course"]

        existing = best_evidence.get(
            course
        )

        if (
            existing is None
            or item["score"] > existing["score"]
        ):

            best_evidence[course] = item

    final_courses = sorted(
        best_evidence.keys()
    )

    final_evidence = list(
        best_evidence.values()
    )

    final_evidence.sort(
        key=lambda item: (
            item["course"],
            -item["score"]
        )
    )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    print("\n========================================")
    print(
        "FINAL COURSES:",
        final_courses
    )
    print(
        "PAGES CHECKED:",
        pages_checked
    )
    print("========================================")

    return {
        "success": True,
        "courses": final_courses,
        "evidence": final_evidence,
        "pages_checked": pages_checked,
        "errors": errors
    }


# =========================================================
# COMPATIBILITY FUNCTION
# =========================================================

def scrape_courses(
    website
):

    result = scrape_courses_detailed(
        website
    )

    return result["courses"]


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    website = input(
        "\nEnter official college website: "
    ).strip()

    result = scrape_courses_detailed(
        website
    )

    print("\n========================================")
    print("RESULT")
    print("========================================")

    print(
        "Courses:",
        result["courses"]
    )

    print(
        "Pages checked:",
        result["pages_checked"]
    )

    print(
        "\nBest Evidence:"
    )

    for item in result["evidence"]:

        print(
            f"\n{item['course']} "
            f"(score={item['score']})"
        )

        print(
            "Source:",
            item["source"]
        )

        print(
            "Text:",
            item["text"]
        )