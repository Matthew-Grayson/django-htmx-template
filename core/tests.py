from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTests(TestCase):
    """Test suite for authentication functionality."""

    def setUp(self):
        """Set up test client and test user."""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass123", email="admin@test.com"
        )

    def test_registration_creates_user(self):
        """Test that registration creates a new user."""
        response = self.client.post(
            reverse("core:register"),
            {
                "username": "newuser",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_logs_user_in(self):
        """Test that registration automatically logs the user in."""
        response = self.client.post(
            reverse("core:register"),
            {
                "username": "newuser",
                "password1": "complexpass123",
                "password2": "complexpass123",
            },
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.context["user"].username, "newuser")

    def test_dashboard_redirects_anonymous_users(self):
        """Test that dashboard redirects anonymous users to login."""
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_dashboard_accessible_to_authenticated_users(self):
        """Test that authenticated users can access dashboard."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, testuser")

    def test_login_with_correct_credentials(self):
        """Test login works with correct credentials."""
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "testpass123"},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_incorrect_credentials(self):
        """Test login fails with incorrect credentials."""
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)  # Stays on login page
        self.assertFalse(response.context["user"].is_authenticated)

    def test_logout(self):
        """Test logout functionality."""
        self.client.login(username="testuser", password="testpass123")
        self.client.post(reverse("logout"))
        # Make a new request to verify user is no longer authenticated
        response = self.client.get(reverse("core:index"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_admin_requires_staff(self):
        """Test that admin endpoint requires staff/superuser."""
        # Anonymous user should be redirected
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

        # Regular user should be redirected to login
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

        # Admin user should have access
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_renders(self):
        """Test that registration page renders correctly."""
        response = self.client.get(reverse("core:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_login_page_renders(self):
        """Test that login page renders correctly."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_dashboard_shows_htmx_demo(self):
        """Test that dashboard includes HTMX demo."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertContains(response, "HTMX Activity Demo")
        self.assertContains(response, "hx-get")

    def test_dashboard_shows_admin_link_for_staff(self):
        """Test that staff users see admin link on dashboard."""
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertContains(response, "Admin Panel")

    def test_dashboard_hides_admin_link_for_regular_users(self):
        """Test that regular users don't see admin link on dashboard."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:dashboard"))
        self.assertNotContains(response, "Admin Panel")

