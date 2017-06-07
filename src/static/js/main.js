/* global converse */
/* global CURRENT_USER_AUTHENTICATED */
/* global CURRENT_USER_FIRST_NAME */
/* global CURRENT_USER_LAST_NAME */

(function() {
    "use strict";
    if (CURRENT_USER_AUTHENTICATED) {
      converse.initialize({
          bosh_service_url: 'https://chatproto.muikkuverkko.fi/http-bind/',
          show_controlbox_by_default: true,
          jid: CURRENT_USER_FIRST_NAME + '.' + CURRENT_USER_LAST_NAME + "@chatproto.muikkuverkko.fi",
          password: "whatever",
          auto_login: true
      });
    }
}());
