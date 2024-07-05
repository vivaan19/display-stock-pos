import logging
from odoo.addons.point_of_sale.tests.test_frontend import TestUi, MobileTestUi
from odoo.tests import loaded_demo_data, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestUiBD(TestUi):
    def test_01_pos_basic_order(self):

        print("\n hiiiiiiiiiiiiiiiii ")
        
        super().test_01_pos_basic_order()
        

class BDMobileTestUi(MobileTestUi):

    print("\n In mob test ---- 2")

    browser_size = '375x667'
    touch_enabled = True