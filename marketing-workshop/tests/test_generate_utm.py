import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import generate_utm  # noqa: E402


class TestValidUrlGeneration(unittest.TestCase):
    def test_appends_all_five_params_in_order(self):
        url = generate_utm.build_utm_url(
            "https://example.com/pricing",
            source="newsletter", medium="email", campaign="launch",
            content="top-cta", term="b2b saas",
        )
        query = urlsplit(url).query
        self.assertEqual(
            query,
            "utm_source=newsletter&utm_medium=email&utm_campaign=launch&utm_content=top-cta&utm_term=b2b+saas",
        )

    def test_omits_params_not_provided(self):
        url = generate_utm.build_utm_url("https://example.com/", source="reddit", medium="community")
        params = parse_qs(urlsplit(url).query)
        self.assertEqual(set(params), {"utm_source", "utm_medium"})

    def test_deterministic_across_calls(self):
        kwargs = dict(source="x", medium="y", campaign="z")
        first = generate_utm.build_utm_url("https://example.com/a", **kwargs)
        second = generate_utm.build_utm_url("https://example.com/a", **kwargs)
        self.assertEqual(first, second)


class TestExistingQueryParameters(unittest.TestCase):
    def test_non_utm_params_are_preserved(self):
        url = generate_utm.build_utm_url(
            "https://example.com/pricing?ref=affiliate123&lang=en",
            source="newsletter",
        )
        params = parse_qs(urlsplit(url).query)
        self.assertEqual(params["ref"], ["affiliate123"])
        self.assertEqual(params["lang"], ["en"])
        self.assertEqual(params["utm_source"], ["newsletter"])


class TestExistingUtmReplacement(unittest.TestCase):
    def test_existing_utm_value_is_replaced_not_duplicated(self):
        url = generate_utm.build_utm_url(
            "https://example.com/?utm_source=old&utm_medium=old",
            source="new",
        )
        params = parse_qs(urlsplit(url).query)
        self.assertEqual(params["utm_source"], ["new"])
        self.assertNotIn("utm_medium", params)

    def test_replacement_preserves_non_utm_order(self):
        url = generate_utm.build_utm_url(
            "https://example.com/?a=1&utm_source=old&b=2",
            source="new",
        )
        self.assertTrue(url.startswith("https://example.com/?a=1&b=2&utm_source=new"))


class TestUrlEncoding(unittest.TestCase):
    def test_spaces_and_special_characters_are_encoded(self):
        url = generate_utm.build_utm_url(
            "https://example.com/",
            campaign="Q3 launch & relaunch",
        )
        self.assertIn("utm_campaign=Q3+launch+%26+relaunch", url)


class TestInvalidUrls(unittest.TestCase):
    def test_missing_scheme_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_utm.build_utm_url("example.com/pricing", source="x")

    def test_missing_host_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_utm.build_utm_url("https:///pricing", source="x")

    def test_non_http_scheme_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_utm.build_utm_url("ftp://example.com/", source="x")


class TestCli(unittest.TestCase):
    def test_main_returns_zero_on_success(self):
        self.assertEqual(generate_utm.main(["https://example.com/", "--source", "x"]), 0)

    def test_main_returns_nonzero_on_invalid_url(self):
        self.assertEqual(generate_utm.main(["not-a-url", "--source", "x"]), 1)


if __name__ == "__main__":
    unittest.main()
