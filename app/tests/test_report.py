def test_admin_access(client, admin_user):
    client.login(admin_user)
    res = client.get('/admin/users')
    assert res.status_code == 200

def test_user_restricted_access(client, regular_user):
    client.login(regular_user)
    res = client.get('/admin/users')
    assert res.status_code == 302
    assert 'недостаточно прав' in res.data.decode('utf-8')