from django import http
from django.core.urlresolvers import reverse
from mox import IsA

from openstack_dashboard import api
from openstack_dashboard.test import helpers as test


class FlavorTemplatesTests(test.BaseAdminViewTests):

    @test.create_stubs({api.tuskar.FlavorTemplate: ('list', 'create')})
    def test_create_flavor_template(self):
        template = self.tuskar_flavor_templates.first()

        api.tuskar.FlavorTemplate.list(
            IsA(http.HttpRequest)).AndReturn([])
        api.tuskar.FlavorTemplate.create(IsA(http.HttpRequest),
                                     template.name,
                                     0, 0, 0, 0, 0).AndReturn(template)
        self.mox.ReplayAll()

        url = reverse(
            'horizon:infrastructure:resource_management:flavors:create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, "infrastructure/resource_management/flavors/create.html")

        data = {'name': template.name,
                'cpu': 0,
                'memory': 0,
                'storage': 0,
                'ephemeral_disk': 0,
                'swap_disk': 0}
        resp = self.client.post(url, data)
        self.assertRedirectsNoFollow(
            resp, reverse('horizon:infrastructure:resource_management:index'))

    @test.create_stubs({api.tuskar.FlavorTemplate: ('list', 'update', 'get')})
    def test_edit_flavor_template_get(self):
        template = self.tuskar_flavor_templates.first()  # has no extra spec

        api.tuskar.FlavorTemplate.get(IsA(http.HttpRequest),
                                  template.id).AndReturn(template)
        self.mox.ReplayAll()

        url = reverse(
            'horizon:infrastructure:resource_management:flavors:edit',
            args=[template.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            resp, "infrastructure/resource_management/flavors/edit.html")

    @test.create_stubs({api.tuskar.FlavorTemplate: ('list', 'update', 'get')})
    def test_edit_flavor_template_post(self):
        template = self.tuskar_flavor_templates.first()  # has no extra spec

        api.tuskar.FlavorTemplate.list(IsA(http.HttpRequest)).AndReturn(
            self.tuskar_flavor_templates.list())
        api.tuskar.FlavorTemplate.update(IsA(http.HttpRequest),
                                     template.id,
                                     template.name,
                                     0, 0, 0, 0, 0).AndReturn(template)
        api.tuskar.FlavorTemplate.get(IsA(http.HttpRequest),
                                  template.id).AndReturn(template)
        self.mox.ReplayAll()

        data = {'flavor_id': template.id,
                'name': template.name,
                'cpu': 0,
                'memory': 0,
                'storage': 0,
                'ephemeral_disk': 0,
                'swap_disk': 0}
        url = reverse(
            'horizon:infrastructure:resource_management:flavors:edit',
            args=[template.id])
        resp = self.client.post(url, data)
        self.assertNoFormErrors(resp)
        self.assertMessageCount(success=1)
        self.assertRedirectsNoFollow(
            resp, reverse('horizon:infrastructure:resource_management:index'))

    @test.create_stubs({api.tuskar.FlavorTemplate: ('list', 'delete')})
    def test_delete_flavor_template(self):
        template = self.tuskar_flavor_templates.first()

        api.tuskar.FlavorTemplate.list(IsA(http.HttpRequest)).\
            AndReturn(self.tuskar_flavor_templates.list())
        api.tuskar.FlavorTemplate.delete(IsA(http.HttpRequest), template.id)
        self.mox.ReplayAll()

        form_data = {'action': 'flavors__delete__%s' % template.id}
        res = self.client.post(
            reverse('horizon:infrastructure:resource_management:index'),
            form_data)

        self.assertRedirectsNoFollow(
            res, reverse('horizon:infrastructure:resource_management:index'))

    @test.create_stubs({api.tuskar.FlavorTemplate: ('get',)})
    def test_detail_flavor_template(self):
        template = self.tuskar_flavor_templates.first()

        api.tuskar.FlavorTemplate.get(IsA(http.HttpRequest),
                                  template.id).AndReturn(template)
        api.tuskar.FlavorTemplate.resource_classes = self. \
            tuskar_resource_classes

        self.mox.ReplayAll()

        url = reverse(
            'horizon:infrastructure:resource_management:flavors:detail',
            args=[template.id])
        res = self.client.get(url)
        self.assertTemplateUsed(
            res, "infrastructure/resource_management/flavors/detail.html")
