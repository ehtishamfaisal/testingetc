# -*- coding: utf-8 -*-
{
    "name"             :  "Website Product Price",
    "category"         :  "Website",
    "version"          :  "0.1",
    "sequence"         :  10,
    "depends"          :  ['website_sale'],
    "data"             :  [
                      'security/ir.model.access.csv',
                       'data/data.xml',
                       'views/website_product_price.xml',
                       'views/template.xml',
                        'views/product_template.xml',
                      ],
    "application"     :  True,
    "installable"     :  True,
}
