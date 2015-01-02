from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
import datetime

from lists.models import Item, List
from lists.views import *

class UserHomePageTest(TestCase):

	def test_root_url_resolves_to_user_login_view(self):
		found = resolve('/')
		self.assertEqual(found.func, user_login)
	
	
	def test_login_page_returns_correct_html(self):
		request = HttpRequest()
		response = user_login(request)
		expected_html = render_to_string('login.html')
		self.assertEqual(response.content.decode(), expected_html)
		
	def test_registration_page(self):
		response = self.client.get(
			'/lists/register/',
		)
		self.assertTemplateUsed(response, 'register.html')
	
	
class ListAndItemModelsTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.name = 'First List'
		list_.save()
		list2_ = List()
		list2_.name = 'Second List'
		list2_.save()
		
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()
		
		third_item = Item()
		third_item.text = 'Item the third'
		third_item.list = list2_
		third_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_lists = List.objects.all()
		self.assertEqual(saved_lists.count(), 2)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 3)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		third_saved_item = saved_items[2]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(first_saved_item.created_date.day, timezone.now().day)
		self.assertEqual(first_saved_item.done, 0)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)
		self.assertEqual(third_saved_item.text, 'Item the third')
		self.assertEqual(third_saved_item.list, list2_)

	
class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create(name = 'alice')
		response = self.client.get('/lists/%s/' % (list_.name,))
		self.assertTemplateUsed(response, 'list.html')

		
	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create(name = 'alice')
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create(name='bob')
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)
		
		response = self.client.get('/lists/%s/' % (correct_list.name,))
		
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create(name = 'alice')
		correct_list = List.objects.create(name = 'bob')
		
		self.client.post(
			'/lists/%s/add_item' % (correct_list.name,),
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create(name = 'alice')
		correct_list = List.objects.create(name = 'bob')
		
		response = self.client.post(
			'/lists/%s/add_item' % (correct_list.name,),
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, '/lists/%s/' % (correct_list.name,))		

'''		
		
class ChangeItemList(TestCase):
	
	def test_mark_item_as_done(self):
	
		list_ = List.objects.create(name='Alice')
		item_ = Item.objects.create(text='One item', list=list_)
		response = self.client.post(
			'/lists/change_item',
			data={'item_id': item_.id, 'done': '2'}
		)
		saved_item = Item.objects.get(id=1)
		self.assertEqual(saved_item.done, 2)
		
		
'''	
	
'''
class NewListTest(TestCase):
	fixtures = ['admin_user.json']
	def test_can_login_to_create_new_list(self):
		
#		user_test = User.objects.create(username = 'admin1', password = 'admin1')
		response = self.client.post(
			'/lists/login/',
			data={'username': 'admin', 'password': 'admin'}
		)
		self.assertEqual(List.objects.count(), 1)
'''