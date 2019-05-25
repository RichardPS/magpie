# Purchase Order System (Magpie)

Allows users to raise a purchase order

Purchase orders over £200 will raise an order, and dependant on the value of the order
their department manager, and for orders over £2000 also the managing director will
be sent an email which will allow them to accept, or decline the order.

#### User Creations options

 * Department (i.e. Production, Sales etc.)
 * Department Manager
 * Accounts Admin (can only be set by superuser)
 * Managing Director (can only be set by superuser)

#### User permissions

 * User
    * Can raise purchase order
    * Can view their own orders
    
 * Department Manager
    * Can raise purchase order
    * Can authorise orders via a link sent in an email

 * Accounts Admin
    * Can view all orders in admin area
    * Can cancel orders
    * Can clear complete orders
    
 * Managing Director
    * Can authorise orders via a link sent in an email


#### Areas of Site

 * Raise Order (login required)
    * Provides form for a logged in user to raise a purchase order
    
 * My Orders (login required)
    * Displays a list fo others for the current logged in user
 
 * Order Admin Area (accounts admin required)
    * Displays a list of all orders
    * Provides the ability to clear and cancel an order
    
 * User Management (django staff or superuser permissions required)
    * Displays all users and roles set
    * Ability to edit users
