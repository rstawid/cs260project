from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
	
    def test_can_log_in_via_admin_site(self):
        #admin goes to admin page
        self.browser.get(self.live_server_url + '/admin/')
        #looks for Django administration
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
        #admin types username & password and hits ENTER
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.ENTER)	
        #username and password accepted, and user is taken to admin page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)
	
	
    def test_can_start_a_list_and_retrieve_it_later(self):
	
        # admin Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

		#user logging in
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.ENTER)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Your To-Do list today', body.text)
		
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
		
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
		
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a 
		# to-do list table
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very 
		# methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's  is coming through from the cookies etc #
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #Alice visits the home page. There is no sign of Edith's
        #list
        self.browser.get(self.live_server_url)
		
		#user logging in
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('alice')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('alice')
        password_field.send_keys(Keys.ENTER)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Your To-Do list today', body.text)
		
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
		
        #Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
		
        #Satisfied, they both go back to sleep