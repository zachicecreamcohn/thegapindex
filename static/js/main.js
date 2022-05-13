
const { createApp } = Vue;


// import VeuxPersist from 'veux-persist';
// Vue.use(VeuxPersist);

const theGapIndexApp = {
    created() {
        let productList = []
        let productData = {}
        fetch('/api/search/shirt')
            .then(response => response.json())
            .then(data => {
                let resultData = data[1]
                this.pageCount = data[0]
                this.productData = resultData
                this.productList = resultData[this.page]
                        // this.productList = productList
                    }
            )
                // }
                


            // })

        },
        
    data() {
        let productList = []

        return {
            errorMessage: '',
            message: '',
            timesCheckedUserInfo: 0,
            timesCheckedLoginStatus: 0,
            productList: [],
            productData: {},
            hoverCart: false,
            loggedIn: false,
            searchInput: '',
            colorSearchInput: '',
            noResults: false,
            page: 1,
            pageCount: 1,
            activateRegister: null,
            regLoginChangeCount : 0,
            skeletonCount: 20,
            cartSkeletonCount: 5,
            numProductsInCart: 0,
            productsInCart: [],
            headerReload: true,
            

            // login data
            loginEmail: '',
            loginPassword: '',

            // register data
            registerFirstName: '',
            registerLastName: '',
            registerEmail: '',
            registerPassword: '',
            registerPhone: '',

            userData: {},
            colors: ['red', 'green', 'blue', 'yellow', 'black', 'white', 'purple', 'orange', 'brown', 'grey', 'pink', 'teal', 'maroon', 'lime', 'tan']
            
        }

        let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
        if (productsInCart) {
            this.productsInCart = productsInCart
            this.numProductsInCart = productsInCart.length
        }



    },
    computed: {
        
        
        
   
        numGAPinCart: function () {
            let numGAPinCart = 0
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                productsInCart.forEach(product => {
                    // if URL begins with 'https://www.gap.com/
                    if (product.URL.includes('https://www.gap.com/')) {
                        numGAPinCart++
                    }
                })
            }
            return numGAPinCart
        },
        numOLDinCart: function () {
            let numOLDinCart = 0
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                productsInCart.forEach(product => {
                    // if URL begins with 'https://oldnavy.gap.com/
                    if (product.URL.includes('https://oldnavy.gap.com/')) {
                        numOLDinCart++
                    }
                })
            }
            return numOLDinCart
        },

        numBANANAinCart: function () {
            let numBANANAinCart = 0
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                productsInCart.forEach(product => {
                    // if URL begins with 'https://bananarepublic.gap.com/
                    if (product.URL.includes('https://bananarepublic.gap.com/')) {
                        numBANANAinCart++
                    }
                })
            }
            return numBANANAinCart
        },

        numATHLETAinCart: function () {
            let numATHLETAinCart = 0
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                productsInCart.forEach(product => {
                    // if URL begins with 'https://athleta.gap.com/
                    if (product.URL.includes('https://athleta.gap.com/')) {
                        numATHLETAinCart++
                    }
                })
            }
            return numATHLETAinCart
        },




        
        productsInCart1: function () {
            if (this.loggedIn) {
                console.log("productsInCart called from loggedIn")
                // get cart from server
                fetch('/get-cart', 
                    {
                        method : 'POST'
                    })
                .then(response => response.json())
                .then(data => {
                    cart = data.cart
                    this.numProductsInCart = cart.length
                    localStorage.setItem('productsInCart', JSON.stringify(cart))
                    return cart

                })
            } else {
                console.log("productsInCart called from not loggedIn")
            }
            return JSON.parse(localStorage.getItem('productsInCart'))
            
        },
       
                
        enableRegister: function () {
            if (this.regLoginChangeCount == 0) {
                if (window.location.pathname === '/login') {
                    this.activateRegister = false

                    return false
                } else if (window.location.pathname === '/register') {
                    this.activateRegister = true
   
                    return true
                } else {
                    return this.activateRegister
                }
            } else {
                return this.activateRegister
            }
        },
        currentPage: function() {
            return this.page
        },
        currentPageProducts: function() {
            return this.productData[this.page]

        },
        
    },

    

    methods: {
        goToAccount: function () {
            window.location.href = '/account'
        },
        // method to upload image to server
        uploadImage: function (event) {
            let uploadInput = document.getElementById('upload-image')
            let file = uploadInput.files[0]
            
            // send file to flask server
            let formData = new FormData()
            formData.append('file', file)
            fetch('/upload-image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                this.userData.imagePath = data.imagePath

            })
        },


        getUserInfo: function () {
            if (this.timesCheckedUserInfo == 0) {
                fetch('/get-user-info')
                    .then(response => response.json())
                    .then(data => {
                        if (data.email) {
                            this.userData = data
                        }
                    })
                
                this.timesCheckedUserInfo++
                return this.userData
            } else {
                return this.userData
            }
        },


        checkLoginStatus() {
            // get localStorage variable 'loggedIn'
            let loggedIn = localStorage.getItem('loggedIn')

            if (loggedIn === 'true') {
                console.log('loggedIn is true')
                this.loggedIn = true
                return true
            } else {
                console.log('loggedIn is false')
                this.loggedIn = false
                return false
            }
            

            
        },
        logout: function() {
            localStorage.setItem('loggedIn', false)
            this.loggedIn = false
            localStorage.setItem('productsInCart', JSON.stringify([]))

            // set html of left-header
            

            fetch('/logout')

            .then(response => response.json())
            .then(data => {
                
                if (data.loggedOut) {
                    this.loggedIn = false
                    // this.productsInCart = []
                    // set localStorage variable 'loggedIn' to false
                    localStorage.setItem('loggedIn', false)
                    this.numProductsInCart = 0
                    localStorage.setItem('productsInCart', JSON.stringify([]))

           
                    window.location.href = '/'
                    // reload
                    // window.location.reload()
               

                    

                    
                }
            })
        },

        login: function () {
            // send a post request to '/login-request'
            
            fetch('/login-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.loginEmail,
                    password: this.loginPassword
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.loggedIn = true
                        this.message = data.message
                        this.loginEmail = ''
                        this.loginPassword = ''
                        this.regLoginChangeCount = 0
                        

                        localStorage.setItem('loggedIn', true)
                        // redirect to home page
                        // setTimeout(() => {
                        
                        // reload
                        // window.location.reload()
                        // }, 200);

                        // set localStorage variable 'loggedIn' to true
                        
                        


                        // get cart from server
                        fetch('/get-cart', {
                            method: 'POST'
                        })
                        .then(response => response.json())
                        .then(data => {
                            cart = data.cart
                            this.numProductsInCart = cart.length
                            localStorage.setItem('productsInCart', JSON.stringify(cart))
                            window.location.href = '/'

                        })
                        


                    } else {
                        this.loggedIn = false
                        this.message = data.message
                        this.loginEmail = ''
                        this.loginPassword = ''
                        this.regLoginChangeCount = 0
                    }
                })
                
        },
        register: function () {
            // send a post request to '/register-request'

            fetch('/register-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    firstName: this.registerFirstName,
                    lastName: this.registerLastName,
                    email: this.registerEmail,
                    password: this.registerPassword,
                    phone: this.registerPhone
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // this.loggedIn = true
                        this.regLoginChangeCount++
                        this.activateRegister = false
                        this.registerFirstName = ''
                        this.registerLastName = ''
                        this.registerEmail = ''
                        this.registerPassword = ''
                        this.registerPhone = ''


                        // get cart from server
                        fetch('/get-cart')
                        .then(response => response.json())
                        .then(data => {
                            cart = data.cart
                            this.numProductsInCart = cart.length
                            localStorage.setItem('productsInCart', JSON.stringify(cart))

                        })

                        this.loggedIn = true
                        localStorage.setItem('loggedIn', true)
                        
                        // redirect to '/'
                        window.location.href = '/' 
                        // reload
                        // window.location.reload()

                        // set localStorage variable 'loggedIn' to true
                        

                    } else {
                        this.errorMessage = data.message
                    }
                })
        },

        openAllLinks: function() {
            let links = []
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))

            // for each product in productsInCart, add product.URL to links
            for (let i = 0; i < productsInCart.length; i++) {
                links.push(productsInCart[i].URL)
            }

            // open all links in new window
            for (let i = 0; i < links.length; i++) {
                window.open(links[i], i)
            }


        },

        
        isInCart: function(product) {
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                for (let i = 0; i < productsInCart.length; i++) {
                    if (productsInCart[i].id === product.id) {
                        return true
                    }
                }
            }
            return false
        },
        showAddToCart: function(product) {
            // add opacity: 1 to id = cart-popup_<product_id>
            let cartPopup = document.getElementById('cart-popup_' + product.id)
            cartPopup.style.opacity = '1'
        },
        hideAddToCart: function(product) {
            // add opacity: 0 to id = cart-popup_<product_id>
            let cartPopup = document.getElementById('cart-popup_' + product.id)
            cartPopup.style.opacity = '0'
        },
        add_remove_ToCart: function(product) {
            let cartIcon = document.getElementById('cart-icon_' + product.id)
            if (this.checkIfInCart(product)) {
                // remove from cart
                removeFromCart(product)

                this.numProductsInCart -= 1

                 // if on cart page, remove from cart
                 if (window.location.pathname === '/cart') {
                    let cartItem = document.getElementById('cart-item_' + product.id)
                    cartItem.remove()

                    // check what company the product is from
                    if (product.URL.includes('https://www.gap.com/')) {
                        let numGap = document.getElementById('num-gap')
                        // get last character of numGap
                        let lastChar = numGap.innerHTML.slice(-1)
                        // make it a number
                        let numGapNum = parseInt(lastChar)
                        // subtract 1 from numGap
                        numGapNum -= 1
                        // replace last character with new number
                        numGap.innerHTML = numGap.innerHTML.slice(0, -1) + numGapNum

                        

                    } else if (product.URL.includes('https://oldnavy.gap.com/')) {
                        let numOld = document.getElementById('num-old')
                        // get last character of numGap
                        let lastChar = numOld.innerHTML.slice(-1)
                        // make it a number
                        let numOldnum = parseInt(lastChar)
                        // subtract 1 from numGap
                        numOldnum -= 1
                        // replace last character with new number
                        numOld.innerHTML = numOld.innerHTML.slice(0, -1) + numOldnum
                        
                    }
                    else if (product.URL.includes('https://bananarepublic.gap.com/')) {
                        let numBanana = document.getElementById('num-banana')
                        // get last character of numGap
                        let lastChar = numBanana.innerHTML.slice(-1)
                        // make it a number
                        let numBanananum = parseInt(lastChar)
                        // subtract 1 from numGap
                        numBanananum -= 1
                        // replace last character with new number
                        numBanana.innerHTML = numBanana.innerHTML.slice(0, -1) + numBanananum
                        
                    }
                    else if (product.URL.includes('https://athleta.gap.com/')) {
                        let numAthleta = document.getElementById('num-athleta')
                        // get last character of numGap
                        let lastChar = numAthleta.innerHTML.slice(-1)
                        // make it a number
                        let numAthletanum = parseInt(lastChar)
                        // subtract 1 from numGap
                        numAthletanum -= 1
                        // replace last character with new number
                        numAthleta.innerHTML = numAthleta.innerHTML.slice(0, -1) + numAthletanum
                        
                    }


                } else {
                cartIcon.src='/static/img/shopping-cart.png'
                }
               
            } else {
                // add to cart
                this.addToCart(product)
                this.numProductsInCart += 1

                
                cartIcon.src = '/static/img/checkmark.svg'
            }
        },

        addToCart: function(product) {
            // a function to add a product to the cart
            
            // get the products in cart from local storage
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                // if there are products in the cart

                // check if the product is already in the cart
                if (!this.checkIfInCart(product)) {
                // add the product to the cart
                productsInCart.push(product)
                // update the local storage
                localStorage.setItem('productsInCart', JSON.stringify(productsInCart))
                // update cart
                let productsInCart1 = JSON.parse(localStorage.getItem('productsInCart'))

                fetch ('/update-cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            cart: productsInCart1
                        })
                    })
                }
                
            } else {
                // if there are no products in the cart
                // create an array and add the product to the cart
                productsInCart = []
                productsInCart.push(product)
                // update the local storage
                let productsInCart1 = JSON.parse(localStorage.getItem('productsInCart'))

                localStorage.setItem('productsInCart', JSON.stringify(productsInCart))
                fetch ('/update-cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            productsInCart: productsInCart1
                        })
                    })
            }

        },
        // removeFromCart: function(product) {
        //     conosle.log('remove from cart CALLED FROM METHOD')
        //     // a function to remove a product from the cart
            
        //     // get the products in cart from local storage
        //     let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
        //     if (productsInCart) {
        //         // if there are products in the cart
        //         // remove the product from the cart

        //         for (let i = 0; i < productsInCart.length; i++) {
        //             if (productsInCart[i].id === product.id) {
        //                 productsInCart.splice(i, 1)
                        
        //             }
        //         }
        //             // update the local storage
        //         localStorage.setItem('productsInCart', JSON.stringify(productsInCart))
        //         // update this.productsInCart
        //         this.productsInCart = productsInCart

        //     // check length of products in cart
        //     let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
        //     if (productsInCart.length === 0) {

        //     }
        //     let productsInCart12 = JSON.parse(localStorage.getItem('productsInCart'))

        //     fetch ('/update-cart', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'
        //             },
        //             body: JSON.stringify({
        //                 cart: productsInCart12
        //             })
        //         })
            

        // }
        // },

        checkIfInCart: function(product) {
            // a function to check if a product is in the cart
            // if (this.loggedIn) {

            // fetch ('/get-cart', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json'
            //         },
                    
            //     })
            // .then(response => response.json())
            // .then(data => {
            //     cart = data.cart
            //     this.productsInCart = cart
            //     // add each item to browser variable productsInCart
                
            //     for (let i = 0; i < this.productsInCart.length; i++) {
            //         console.log(this.productsInCart[i].id)
            //         console.log(product.id)
            //         if (this.productsInCart[i].id == product.id) {
            //             return true
            //         }
            //     }

            //     return false
            // })
            // } else {
            let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
            if (productsInCart) {
                for (let i = 0; i < productsInCart.length; i++) {
                    if (productsInCart[i].id === product.id) {
                        return true
                    }
                }
            }
            return false

        // }
        },
        // removeFromCart: function(product) {
        //     // remove product from cart

        //     //replace id 'cart-icon_<product_id>' with img of a cart
        //     let cartIcon = document.getElementById('cart-icon_' + product.id)
        //     cartIcon.src = '/static/img/shopping-cart.png'
        // },
        getID(product) {
            // get the id of the product
            return product.id
        },
        goToProduct: function(URL) {
            // open URL in new tab
            window.open(URL, '_blank');
        },
        openCart: function() {
            // go to '/cart'
            window.location.href = '/cart'
        },
        goHome: function() {
            window.location.href = '/'
        },
        openRegister() {
            this.regLoginChangeCount = 1
            this.activateRegister = true
        },
        openLogin() {
            this.regLoginChangeCount = 1
            this.activateRegister = false
        },
        nextPage: function() {
            if (this.page <= this.pageCount) {
                this.page += 1      
            } else {
                this.page = 1
            }  
            // send user to top of page
            window.scrollTo(0, 0)
        },
        prevPage: function() {
            if (this.page > 1) {
                this.page -= 1
            } else {
                this.page = 1
            }
            // send user to top of page
            window.scrollTo(0, 0)
        },
        filterByColor: function() {

            color = this.colorSearchInput
            console.log(color)
            search_term = this.searchInput

            if (search_term !== '') {
                // if there is a search term
                // send the search term and color to the server
                fetch ('/api/search-by-color-and-term', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            search_term: search_term,
                            color: color
                        })
                    })
                .then(response => response.json())
                .then(data => {
                    resultData = data[1]
                    this.pageCount = data[0]
                    this.productData = resultData
                    this.productList = resultData[this.page]

                    if (!data) {
                        this.noResults = true
                    } else {
                        this.noResults = false
                        this.page = 1
                    }
                })
            }
        },



        searchAction: function() {

            if (this.searchInput.length > 0) {
                fetch('/api/search/' + this.searchInput)
                    .then(response => response.json())
                    .then(data => {
                        resultData = data[1]
                        this.pageCount = data[0]
                        this.productData = resultData
                        this.productList = resultData[this.page]

                        if (!data) {
                            this.noResults = true
                        } else {
                            this.noResults = false
                            this.page = 1
                        }
                    })
                    // catch error
                    .catch(error => {
                        console.log("shit")
                    })

                }

        },
    },
    delimiters: ['[[', ']]'],


}

setHeaderLinks();


createApp(theGapIndexApp).mount('#app');

loginStatus();
setPageNum();

function setPageNum() {
    // get url parameter 'page'
    let urlParams = new URLSearchParams(window.location.search);
    let page = urlParams.get('page');
    if (page) {
        // make page a number
        page = parseInt(page)

        theGapIndexApp.page = page
    } else {
        theGapIndexApp.page = 1
    }
    
}



function removeFromCart(product) {
    // a function to remove a product from the cart
    
    // get the products in cart from local storage
    let productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
    if (productsInCart) {
        // if there are products in the cart
        // remove the product from the cart

        for (let i = 0; i < productsInCart.length; i++) {
            if (productsInCart[i].id === product.id) {
                productsInCart.splice(i, 1)
            }
        }
            // update the local storage
        localStorage.setItem('productsInCart', JSON.stringify(productsInCart))
        // also update this.productsInCart
        theGapIndexApp.productsInCart = productsInCart

        // update cart on server
        fetch ('/update-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    cart: productsInCart
                })

            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            })
    

    // check length of products in cart
    // if url is '/cart' 
    if (window.location.pathname === '/cart') {
    productsInCart = JSON.parse(localStorage.getItem('productsInCart'))
    if (productsInCart.length === 0) {
        let buynow = document.getElementById('buynowcontainer')
        buynow.style.display = 'none'
        let emptyMessageHTML = `<div id="empty-cart-message" v-if='productsInCart.length == 0'>
        <h2>Your cart is empty</h3>
        <p>Add some products to your cart</p>
    </div>`
        // add empty cart message to id 'content' 
        document.getElementById('content').innerHTML = emptyMessageHTML


    }
}


    } else {
        // if there are no products in the cart
        // do nothing
    }
}
    


// function checkLogin() {
//     // send a request to '/check-login'
    
//     fetch('/check-login')
//         .then(response => response.json())
//         .then(data => {
//             return data.loggedIn
//         })

// }


function loginStatus() {
    if (this.timesCheckedLoginStatus === 0) {
    fetch('/check-login')
        .then(response => response.json())
        .then(data => {
            if (data.loggedIn) {
                console.log('logged in')
                // this.loggedIn = true
                theGapIndexApp.loggedIn = true
            } else {
                console.log('not logged in')
                // this.loggedIn = false
                theGapIndexApp.loggedIn = false
            }
        })
        this.timesCheckedLoginStatus += 1
    }
    return this.loggedIn
}


function setHeaderLinks() {
    // check if user is logged in

    let leftHeader = document.getElementById('left-header')
    
    let profileLink = document.getElementById('profile-link')
    let registerLink = document.getElementById('register-link')
    let loginLink = document.getElementById('login-link')
    let logoutLink = document.getElementById('logout-link')
    fetch ('/check-login')
    .then(response => response.json())
    .then(data => {
        if (data.loggedIn) {
            this.loggedIn = true

            localStorage.setItem('loggedIn', true)
            // if user is logged in
            // show profile link
            // profileLink.style.display = 'block'
            // registerLink.style.display = 'none'
            // loginLink.style.display = 'none'
            // logoutLink.style.display = 'block'
        } else {
            this.loggedIn = false
            localStorage.setItem('loggedIn', false)
            // if user is not logged in
            // show register and login links
            // profileLink.style.display = 'none'
            // registerLink.style.display = ''
            // loginLink.style.display = ''
            // logoutLink.style.display = 'none'
        }
    })
}
