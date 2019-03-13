from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos',
                    cpf='21-99618-6180',
                    email='henrique@bastos.net',
                    phone='21-099345-23554')
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscriptioin_from(self):
        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com',
                  'henrique@bastos.net']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = ['Henrique Bastos',
                    '21-99618-6180',
                    'henrique@bastos.net',
                    '21-099345-23554'
                    ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)