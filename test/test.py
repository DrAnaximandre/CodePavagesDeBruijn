import json

class TestClass:

    with open("configs/config_tests.json", 'r') as config_file:
        config = json.load(config_file)


    def test_goPolo(self):

        from go import goPolo
        h = goPolo(self.config)
        assert h == "589039d3f8ba2f7b714b292aaaa22cca"