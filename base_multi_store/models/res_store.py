# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api


class res_store(models.Model):
    _name = "res.store"
    _description = 'Stores'
    _order = 'parent_id desc, name'

    name = fields.Char(
        'Name',
        required=True,
    )
    parent_id = fields.Many2one(
        'res.store',
        'Parent Store',
        select=True
    )
    child_ids = fields.One2many(
        'res.store',
        'parent_id',
        'Child Stores'
    )
    company_id = fields.Many2one(
        'res.company', 'Company',
        # required=True,
        help='If specified, this store will be only available on selected '
        'company',
    )
    user_ids = fields.Many2many(
        'res.users',
        'res_store_users_rel',
        'cid', 'user_id',
        'Users'
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name, company_id)',
            'The store name must be unique per company!')
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context = dict(self.env.context or {})
        if context.pop('user_preference', None):
            store_ids = list(set(
                [self.env.user.store_id.id] + [cmp.id for cmp in self.env.user.store_ids]))
            args = (args or []) + [('id', 'in', store_ids)]
        return super(res_store, self).name_search(name=name, args=args, operator=operator, limit=limit)
