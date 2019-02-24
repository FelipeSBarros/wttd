from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get("/inscricao/")

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must return subscriptions/subscription_form.html"""
        response = self.client.get("/inscricao/")
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """html must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        "html mst contaian csrf"
        self.assertContains(self.resp, "csrfmiddlewaretoken")

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context["form"]
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """"Form must have 4 fields"""
        form = self.resp.context["form"]
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',
                    cpf='21-99618-6180',
                    email='henrique@bastos.net',
                    phone='21-099345-23554')
        self.resp = self.client.post('/inscricao/', data)

    def teste_post(self):
        """Valid POST redirect to  /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscriptioin_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com',
                  'henrique@bastos.net']
        self.assertEqual(expect, email.to)

    def test_subscription_email_cody(self):
        email = mail.outbox[0]
        self.assertIn('Henrique Bastos', email.body)
        self.assertIn('21-99618-6180', email.body)
        self.assertIn('henrique@bastos.net', email.body)
        self.assertIn('21-099345-23554', email.body)

class SubscribeInvalisPOst(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/')

    def test_post(self):
        """"Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        """Must confirm subscription"""
        data = dict(name='Henrique Bastos',
                    cpf='12345678901',
                    email='henrique@bastos.net',
                    phone='21-099345-23554')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, "Inscrição realizada com sucesso!")