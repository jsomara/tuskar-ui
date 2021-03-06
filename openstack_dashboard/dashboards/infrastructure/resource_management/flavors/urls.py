# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls.defaults import patterns, url

from .views import (CreateView, DetailView, EditView,
                    DetailEditView, ActiveInstancesDataView)


FLAVORS = r'^(?P<flavor_id>[^/]+)/%s$'
VIEW_MOD = 'openstack_dashboard.dashboards.infrastructure.' \
    'resource_management.flavors.views'

urlpatterns = patterns(VIEW_MOD,
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(FLAVORS % 'edit/$', EditView.as_view(), name='edit'),
    url(FLAVORS % 'detail_edit/$',
        DetailEditView.as_view(), name='detail_edit'),
    url(FLAVORS % 'detail', DetailView.as_view(), name='detail'),
    url(FLAVORS % 'active_instances_data',
        ActiveInstancesDataView.as_view(), name='active_instances_data')
)
