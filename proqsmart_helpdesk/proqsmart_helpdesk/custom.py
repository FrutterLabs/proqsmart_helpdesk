import frappe
import json

@frappe.whitelist()
def create_ticket(data):
    data_dict = json.loads(data)
    
    new_ticket = frappe.get_doc({
                'subject': data.get('subject',''),
                'raised_by': data.get('raised_by',''),
                'ticket_type': data.get('ticket_type',''),
                'priority' : data.get('priority',''),
                'description': data.get('description','')
                })
    new_ticket.insert()
    
    # {
    #     'data':{
    #         'subject': 'subject',
    #         'raised_by': 'raised_by',
    #         'ticket_type': 'ticket_type',
    #         'priority': 'priority',
    #         'description': 'description'
    #     }
            
    # }