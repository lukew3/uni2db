import unittest
from lib import req_parser

# print(req_parser('2331', 'CSE'))

class TestReqParser(unittest.TestCase):

    """
    def test_empty(self):
        result = req_parser('', 'CSE')
        expected = ''
        self.assertEqual(result, expected)
    """

    def test_single_no_subject(self):
        result = req_parser('2331', 'CSE')
        expected = 'CSE 2331'
        self.assertEqual(result, expected)

    def test_single_with_subject(self):
        result = req_parser('SLAVIC 5450', 'YIDDISH')
        expected = 'SLAVIC 5450'
        self.assertEqual(result, expected)

    def test_double_one_subject(self):
        result = req_parser("Slavic 3310 or 3320", "YIDDISH")
        expected = {
            "type": "OR",
            "items": [
                "SLAVIC 3310",
                "SLAVIC 3320"
            ]
        }
        self.assertEqual(result, expected)

    def test_or_2(self):
        result = req_parser('371 or JewshSt 3371', 'YIDDISH')
        expected = {
            "type": "OR",
            "items": [
                "YIDDISH 371",
                "JEWSHST 3371"
            ]
        }
        self.assertEqual(result, expected)

    """
    def test_one_course_in(self):
        result = req_parser("One course in CompStd, WGSSt, or AfAmASt", "WGSST")
        expected = "ONE COURSE IN COMPSTD, WGSST, OR AFAMAST"
        self.assertEqual(result, expected)
    """

    def test_or_ands(self):
        result = req_parser("1110, 3575, and Sr standing in WGSSt major or minor; or permission of instructor", "WGSST")
        expected = {
            "type": "OR",
            "items": [
                {
                    "type": "AND",
                    "items": [
                        "WGSST 1110",
                        "WGSST 3575",
                        "SR STANDING IN WGSST MAJOR OR MINOR"
                    ]
                },
                "PERMISSION OF INSTRUCTOR"
            ]
        }
        self.assertEqual(result, expected)

    def test_weird_or(self):
        result = req_parser("1110, 3 credit hours in WGSSt courses, or permission of instructor", "WGSST")
        expected = {
            "type": "OR",
            "items": [
                "WGSST 1110",
                "3 CREDIT HOURS IN WGSST COURSES",
                "PERMISSION OF INSTRUCTOR"
            ]
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
