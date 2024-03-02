import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if random.random() < damping_factor and len(corpus[page]) > 0:
        # with P(damping_factor) given the page has links, distribute probability across each link from the page
        return {link: 1 / len(corpus[page]) for link in corpus[page]}
    else:
        # with P(1 - damping_factor) or if the page had no links, distribute probability across all pages
        return {link: 1 / len(corpus) for link in corpus}


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_visits = {}
    # select the initial page at random
    last_page = random.choice(list(corpus.keys()))
    page_visits[last_page] = 1
    # iterate n-1 times (first iteration was selecting the first page)
    for i in range(n - 1):
        next_page = get_next_page(corpus, last_page, damping_factor)
        page_visits[next_page] = page_visits.get(next_page, 0) + 1
        last_page = next_page
    # pageranks = {page: visits / n for page, visits in page_visits.items()}
    return calculate_page_ranks_from_visits(page_visits)


def calculate_page_ranks_from_visits(page_visits):
    # calculate pageranks by normalising against the total number of visits
    total_visits = sum(page_visits.values())
    return {page: visits / total_visits for page, visits in page_visits.items()}


def get_next_page(corpus, last_page, damping_factor):
    probabilities = transition_model(corpus, last_page, damping_factor)
    pages = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(pages, weights=weights, k=1)[0]


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # init ranks
    old_ranks = {page: 1 / len(corpus) for page in corpus}
    new_ranks = calculate_new_ranks(corpus, old_ranks, damping_factor)
    # iterate until close enough to the previous result
    while not is_close_enough(corpus, new_ranks, old_ranks, 0.001):
        old_ranks = new_ranks
        new_ranks = calculate_new_ranks(corpus, old_ranks, damping_factor)
    return new_ranks


def calculate_new_ranks(corpus, old_ranks, d):
    new_ranks = {}
    N = len(corpus)
    for page in corpus:
        # the easy part - using (1 - damping factor) to randomly choose a page
        pr_part_at_random = 1 / N

        # linking_pages: a list of all pages that link to the current page
        linking_pages = [
            linking_page
            for linking_page, linking_page_links in corpus.items()
            if page in linking_page_links
        ]
        pages_that_have_no_links = [page for page in corpus if len(corpus[page]) == 0]

        # sum over the likelihood that the linking pages send the user to the page
        pr_by_linking_pages = sum(
            old_ranks[linking_page] / len(corpus[linking_page])
            for linking_page in linking_pages
        )
        # pages with no links are special - assume they have a link to every page (inc themselves)
        pr_by_pages_with_no_links = sum(
            old_ranks[no_link_page] / N for no_link_page in pages_that_have_no_links
        )

        # calculate the new rank
        new_ranks[page] = ((1 - d) * pr_part_at_random) + (
            d * (pr_by_linking_pages + pr_by_pages_with_no_links)
        )
    return new_ranks


def is_close_enough(corpus, new_ranks, old_ranks, threshold):
    # check all pages present in both
    for page in corpus:
        if page not in new_ranks or page not in old_ranks:
            return False

    # check the diff between old and new pages
    for page in new_ranks:
        if abs(new_ranks[page] - old_ranks[page]) > threshold:
            return False

    # no issues - must be close enough
    return True


if __name__ == "__main__":
    main()
