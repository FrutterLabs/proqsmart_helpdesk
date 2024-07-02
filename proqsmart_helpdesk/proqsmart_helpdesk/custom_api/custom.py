import frappe
import frappe.desk.query_report as reports
import re

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
        
def apply_filters(final_data, filters):
        final_list = []
        for item in final_data:
            filter_flag = True
            for filter_name, filter_value in filters.items():
                # Check if the item has the filter_name key and if its value is not None
                if isinstance(filter_value, list):
                    if item.get(filter_name) not in filter_value:
                        filter_flag = False
                        break
                elif item.get(filter_name) != filter_value:
                    filter_flag = False
                    break
            if filter_flag:
                final_list.append(item)
        return final_list


def apply_search(final_data, search_key):
   final_list = []
   for item in final_data:
       if search_dictionary(item, search_key):
           final_list.append(item)
   return final_list


def apply_search_sort_filters(final_data,order_by,filters,search_key):
   if len(filters) == 0 and search_key == '' and order_by == 'creation desc':
       return final_data
   elif len(filters) > 0 and search_key == '':
       final_data = apply_filters(final_data, filters)
   elif len(filters) == 0 and search_key != '':
       final_data = apply_search(final_data, search_key)
   else:
       final_data = apply_filters(final_data, filters)
       final_data = apply_search(final_data, search_key)
   if order_by != 'creation desc':
       final_data = sorted_results(final_data,order_by)
       return final_data
   
def get_supplier_auction_status_count(self, company_id):
       filters = {'company':company_id}
       data = reports.run(self)
       data['result'] = apply_filters(data['result'],filters=filters)
       return data['result']
   
def search_dictionary(data, query):
        """
        Args:
            data (str): string data
            query (str): search key to find query in data passed


        Returns:
            match : True or False
        """
        data_string = str(data)
        regex = re.compile(query, re.IGNORECASE)
        match = regex.search(data_string)
        return match is not None
    
def get_column_value(item, column):
    return item.get(column)
    
def sorted_results(results, order_by):
    order_by_column, order_by_direction = order_by.split(' ')
    sorted_list = sorted(results, key=lambda x: get_column_value(x, order_by_column), reverse=(order_by_direction == 'desc'))
    return sorted_list