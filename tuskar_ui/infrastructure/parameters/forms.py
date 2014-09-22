# -*- coding: utf8 -*-
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

import logging

import django.forms
from django.utils.translation import ugettext_lazy as _
import horizon.exceptions
import horizon.forms
import horizon.messages

from tuskar_ui import api
import tuskar_ui.api.tuskar
import tuskar_ui.forms


LOG = logging.getLogger(__name__)


class EditServiceConfig(horizon.forms.SelfHandlingForm):
    def __init__(self, *args, **kwargs):
        super(EditServiceConfig, self).__init__(*args, **kwargs)
        self.plan = api.tuskar.Plan.get_the_plan(self.request)
        self.fields.update(self._service_config_fields(self.plan))

    def _service_config_fields(self, plan):
        fields = {}
        for p in self._param_list():
            field = django.forms.CharField(
                label=p.get('name'),
                required=False,
            )
            fields[p.get('name')] = field
        return fields

    def _param_list(self):
	return [{'name':'fakepassword'}]
    
    def handle(self, request, data):
        parameters = dict(
            (name, data[name])
            for (name, field) in self.fields.items()
        )
        try:
            self.plan.patch(request, self.plan.uuid, parameters)
        except Exception as e:
            horizon.exceptions.handle(request, _("Unable to update the service configuration."))
            LOG.exception(e)
            return False
        else:
            horizon.messages.success(request, _("Service configuration updated."))
            return True


