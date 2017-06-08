/* global converse */
/* global CURRENT_USER_AUTHENTICATED */
/* global CURRENT_USER_FIRST_NAME */
/* global CURRENT_USER_LAST_NAME */

(function() {
    "use strict";
     converse.initialize({
          bosh_service_url: 'https://chatproto.muikkuverkko.fi/http-bind/',
          show_controlbox_by_default: true,
          authentication: "login",
          keepalive: "true",
          credentials_url: "/credentials",
          auto_login: true
     });
}());
