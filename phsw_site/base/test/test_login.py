from django.urls import reverse
import pytest
from model_bakery import baker
from phsw_site.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp(client, db):
    return client.get(reverse('login'))


@pytest.fixture
def usuario(db, django_user_model):
    usuario_modelo = baker.make(django_user_model)
    senha = "SenhaAliatoria123@"
    usuario_modelo.set_password(senha)
    usuario_modelo.save()
    usuario_modelo.senha_plana = senha
    return usuario_modelo


@pytest.fixture
def resp_post(client, usuario):
    return client.post(reverse('login'), {'username': usuario.email, 'password': usuario.senha_plana})


def test_login_form_page(resp):
    assert resp.status_code == 200


def test_login_redirect(resp_post):
    assert resp_post.status_code == 302  # status code de redirecionamento
    assert resp_post.url == "/"


@pytest.fixture
def resp_home(client, db):
    return client.get(reverse('base:home'))


def test_botao_entrar_disponivel(resp_home):
    assert_contains(resp_home, 'Entrar')


def test_link_de_login_disponivel(resp_home):
    assert_contains(resp_home, reverse('login'))


@pytest.fixture
def resp_home_com_usuario_logado(client_with_logged_user, db):
    return client_with_logged_user.get(reverse('base:home'))


def test_botao_entrar_indisponivel(resp_home_com_usuario_logado):
    assert_not_contains(resp_home_com_usuario_logado, 'Entrar')


def test_link_de_login_indisponivel(resp_home_com_usuario_logado):
    assert_not_contains(resp_home_com_usuario_logado, reverse('login'))


def test_botao_sair_disponivel(resp_home_com_usuario_logado):
    assert_contains(resp_home_com_usuario_logado, 'Sair')


def test_nome_usuario_logado_disponivel(resp_home_com_usuario_logado, logged_user):
    assert_contains(resp_home_com_usuario_logado, logged_user.first_name)


def test_link_de_logout_disponivel(resp_home_com_usuario_logado):
    assert_contains(resp_home_com_usuario_logado, reverse('logout'))
