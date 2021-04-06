{
    'name': "MO Project code",

    'description': """ When user creates product quotation from sale that order goes in manufacruring 
      order if product is set to Replanish and Manufacturing also product have atleast one 
      bill of matarial. In this module we added the project code text field in quotation form 
      and this field value will be shown in Manufacturing order automatically """,

    'summary': """1.This model is to add project code in quotation from sale order
                  2. It will show project code automatically in manufacturing order also it will be
                    editable """,


    'author': "Techspawn Solutions Pvt. Ltd.",
    'websites': "http://www.techspawn.com",
    'depends': ['sale','mrp'],
    'installable': True,
    'data': [
            'views/sale_order.xml',
            'views/mrp_production.xml',
    ],

}