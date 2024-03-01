from odoo import models, fields, api


class SaleApp(models.Model):
    _inherit = "sale.order"



# @api.multi
    def action_confirm(self):
            res = super(SaleApp, self).action_confirm()

            for order in self:
                product_lines = {}  
                for line in order.order_line:
                    product = line.product_id
                    if product in product_lines:
                        product_lines[product].append(line)
                    else:
                        product_lines[product] = [line]

                for product, lines in product_lines.items():
                    picking_type =self.env['stock.picking.type'].search([('code','=','outgoing')],limit=1)
                    delivery_vals = {
                        'origin': order.name,
                        'partner_id': order.partner_id.id,
                        'location_id': order.warehouse_id.lot_stock_id.id,
                        'location_dest_id': order.partner_id.property_stock_customer.id,
                        'picking_type_id':picking_type.id
                    }

                    delivery = self.env['stock.picking'].create(delivery_vals)

                    for line in lines:
                        move_vals = {
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'product_uom_qty': line.product_uom_qty,
                            'product_uom': line.product_uom.id,
                            'picking_id': delivery.id,
                            'location_id': order.warehouse_id.lot_stock_id.id,
                            'location_dest_id': order.partner_id.property_stock_customer.id,
                        }

                        we =self.env['stock.move'].create(move_vals)
            return res

