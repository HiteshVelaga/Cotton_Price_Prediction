const topAppBar = new mdc.topAppBar.MDCTopAppBar(document.querySelector('.mdc-top-app-bar'));

const MDCButtons = document.querySelectorAll('.mdc-button');
for(var i = 0; i < MDCButtons.length; i++)
    mdc.ripple.MDCRipple.attachTo(MDCButtons[i]);

const MDCTextFields = document.querySelectorAll('.mdc-text-field');
for(var i = 0; i < MDCTextFields.length; i++)
    mdc.textField.MDCTextField.attachTo(MDCTextFields[i]);

const selects = document.querySelectorAll('.mdc-select')
var mdcSelects = new Array()
for(var i = 0; i < selects.length; i++) {
    mdcSelects.push(new mdc.select.MDCSelect(selects[i]))  
}

const tabbar = new mdc.tabBar.MDCTabBar(document.querySelector('.mdc-tab-bar'));