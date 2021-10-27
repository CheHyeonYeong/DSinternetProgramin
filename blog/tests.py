from .models import Post
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_james = User.objects.create_user(username='James', password='somepassword')
        self.user_moha = User.objects.create_user(username='moha', password='somepassword')

    def navbar_test(self, soup):
        # 네비게이션 바가 있는가
        navbar = soup.nav
        # 네비게이션 바에 blog, About me라는 문구가 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo = navbar.find('a', text='Internet Programing')
        self.assertEqual(logo.attrs['href'], '/')
        home = navbar.find('a', text='Home')
        self.assertEqual(home.attrs['href'], '/')
        blog = navbar.find('a', text='Blog')
        self.assertEqual(blog.attrs['href'], '/blog/')
        about = navbar.find('a', text='About Me')
        self.assertEqual(about.attrs['href'], '/about_me')

    def test_post_List(self):
        # 포스트 목록 페이지를 가져온다.
        respons = self.client.get("/blog/")
        # 정상적으로 페이지가 로드되는가
        self.assertEqual(respons.status_code, 200)

        # 페이지 타이플 'blog'
        soup = BeautifulSoup(respons.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        self.navbar_test(soup)
        # 포스트 게시물이 하나도 없는 경우
        self.assertEqual(Post.objects.count(), 0)

        # 적절한 안내문구가 포함되어 있는지
        main_area = soup.find("div", id="main-area")
        self.assertIn("아직 게시물이 없습니다.", main_area.text)

        # 포스트가 2개로 존재하는 경우
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content="wordl hey bye!! we are the world",
            author=self.user_james

        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content=" we are the world",
            author=self.user_moha

        )
        self.assertEqual(Post.objects.count(), 2)

        # 목록 페이지를 새롭게 불러와서
        respons = self.client.get("/blog/", follow=True)
        self.assertEqual(respons.status_code, 200)
        soup = BeautifulSoup(respons.content, 'html.parser')
        # 포스트의 타이틀이 2개 존재
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
        self.assertIn(self.user_james.username.upper(), main_area.text)
        self.assertIn(self.user_moha.username.upper(), main_area.text)

    def test_post_detail(self):
        # 포스트 하나
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content="wordl hey bye!! we are the world",
            author=self.user_james,

        )
        # 이 포스트의 url /blog/1
        self.assertEqual(post_001.get_absolute_url(), '/blog/1')
        # url에 의해 정상적으로 상세페이지를 불러오는가
        respons = self.client.get("/blog/1/")
        self.assertEqual(respons.status_code, 200)
        soup = BeautifulSoup(respons.content, 'html.parser')
        self.navbar_test(soup)

        # 포스트의 title은 웹 브라우저의 title에 있는가
        self.assertIn(post_001.title, soup.title.text)
        # 포스트의 title은 포스트영역에도 있는가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 포스트 작성자가 있는가
        # 아직 작성중
        # 포스트의 내용이 있는가
        self.assertIn(post_001.content, post_area.text)

        self.assertIn(self.user_james.username.upper(), post_area.text)
