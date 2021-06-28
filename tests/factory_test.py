
# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### -----------------------------------------------------------
###  Modified by DevOps Course Summer 2021 Customer Team 
###  Members:
###     Du, Li | ld2342@nyu.edu | Nanjing | GMT+8
###     Cai, Shuhong | sc8540@nyu.edu | Shanghai | GMT+8
###     Zhang, Teng | tz2179@nyu.edu | Ningbo | GMT+8
###     Zhang, Ken | sz1851@nyu.edu | Shanghai | GMT+8
###     Wang,Yu-Hsing | yw5629@nyu.edu | Taiwan | GMT+8
### -----------------------------------------------------------

"""
Test Factory to make fake objects for testing
"""

import factory
import uuid
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText
from service.models import Customer, Address

class AddressFactory(factory.Factory):
    """ 
    Create fake addresses
    """
    class Meta:
        model = Address
    id = factory.Sequence(lambda n: n)
    street = FuzzyChoice(choices=["Century Avenue", "Lafayette Street"])
    apartment = FuzzyChoice(["1555", "383"])
    city = FuzzyChoice(["Shanghai City", "New York City"])
    state = FuzzyChoice(["SH", "NY"])
    zip_code = FuzzyChoice(["200122", "10003"])
    customer_id = factory.Sequence(lambda n: n)


class CustomerFactory(factory.Factory):
    """
    Create fake customers
    """
    class Meta:
        model = Customer
    customer_id = factory.Sequence(lambda n: n)
    first_name = FuzzyChoice(["Wenhan", "Russell"])
    last_name = FuzzyChoice(["Wang", "Solomon"])
    user_id = FuzzyText(uuid.uuid4().hex[:6])
    password = FuzzyChoice(["123456", "abcdef"])
    active = True
    address_id = factory.Sequence(lambda n: n)


if __name__ == '__main__':
    for _ in range(20):
        customer = CustomerFactory()
        address = AddressFactory()