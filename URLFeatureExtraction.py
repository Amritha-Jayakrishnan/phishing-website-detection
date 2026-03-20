import re
from urllib.parse import urlparse
from datetime import datetime
import whois

def get_domain_age(url):
    try:
        domain = url.split("//")[-1].split("/")[0]
        w = whois.whois(domain)

        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return 0

        age_days = (datetime.now() - creation_date).days
        return age_days

    except:
        return 0


def extract_features(url: str):
    parsed = urlparse(url)
    hostname = parsed.netloc
    path = parsed.path

    features = {}

    # Basic features
    features["length_url"] = len(url)
    features["length_hostname"] = len(hostname)
    features["ip"] = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", hostname) else 0

    features["nb_dots"] = url.count(".")
    features["nb_hyphens"] = url.count("-")
    features["nb_at"] = url.count("@")
    features["nb_qm"] = url.count("?")
    features["nb_and"] = url.count("&")
    features["nb_eq"] = url.count("=")

    features["nb_www"] = 1 if "www" in hostname else 0
    features["https_token"] = 1 if "https" in hostname else 0

    # Ratios
    digits = sum(c.isdigit() for c in url)
    features["ratio_digits_url"] = digits / max(len(url), 1)

    # Domain features
    features["domain_age"] = get_domain_age(url)

    # Fill missing expected features
    default_cols = [
        "nb_redirection", "nb_external_redirection",
        "length_words_raw", "char_repeat",
        "shortest_words_raw", "longest_words_raw",
        "avg_words_raw", "phish_hints",
        "domain_in_brand", "brand_in_path",
        "suspecious_tld", "statistical_report",
        "nb_hyperlinks", "ratio_intHyperlinks",
        "ratio_extHyperlinks", "ratio_nullHyperlinks",
        "nb_extCSS", "ratio_intRedirection",
        "ratio_extRedirection", "ratio_intErrors",
        "ratio_extErrors", "login_form",
        "external_favicon", "links_in_tags",
        "submit_email", "ratio_intMedia",
        "ratio_extMedia", "sfh", "iframe",
        "popup_window", "safe_anchor",
        "onmouseover", "right_clic",
        "empty_title", "domain_in_title",
        "domain_with_copyright",
        "whois_registered_domain",
        "domain_registration_length",
        "web_traffic", "dns_record",
        "google_index", "page_rank"
    ]

    for col in default_cols:
        features[col] = 0

    return features