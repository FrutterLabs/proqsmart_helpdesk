import frappe

@frappe.whitelist()
def update_ticket(data):
    doc_id = data.get('name', '')
    updates = data
    
    if not doc_id:
        frappe.local.response["message"] = {
            'success_code': 0,
            'message': 'Ticket ID(name) is missing'
        }
        return

    if not updates:
        frappe.local.response["message"] = {
            'success_code': 0,
            'message': 'No updates provided',
            'updates':updates
        }
        return

    try:
        doc = frappe.get_doc('HD Ticket', doc_id)
        
        for key, value in updates.items():
            if hasattr(doc, key):
                setattr(doc, key, value)
        
        doc.save()
        
        # Adding a comment if 'comment' is provided
        comment = updates.get('comment', '')
        if comment:
            doc.add_comment('Comment', text=comment)
            doc.save()

        frappe.local.response["message"] = {
            'success_code': 1,
            'message': f'Ticket ID - {doc_id} updated successfully'
        }
    except frappe.DoesNotExistError:
        frappe.local.response["message"] = {
            'success_code': 0,
            'message': 'Ticket ID does not exist'
        }
    except Exception as e:
        frappe.local.response["message"] = {
            'success_code': 0,
            'message': f'Something went wrong: {str(e)}'
        }