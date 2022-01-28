Odoo 13.0 (Enterprise Edition) 

Installation 
============
* Install the Application => Apps -> Product Lot Size (Technical Name: product_lot_size)

Product Lot Size
=================

-> The module delivers a facility of creating multiple Manufacturing Orders (MO) as per the size set on the Product.
-> Following things are to be kept in mind while creating MO for eery Stockable Product:
    1. Make sure the Product has set a Reordering Rule with a minimum quantity of the product greater than it's Onhand Quantity.
    2. A Bill of Material of the respective product is a must thing.
    3. The Product Route has to be Manufacture.

Note: The functionality is only developed for the MO being created from Schedulers and not during manual creation of any MOs.
