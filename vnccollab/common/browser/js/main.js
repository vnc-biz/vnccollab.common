// module definition
var vnc_collab_common = (function () {

  // Private components
  function initDeferredPortlets() {

    function deferredUrlInfo(elem) {
      var $elem = jq(elem);
      var manager = $elem.attr('portlet-manager');
      var name    = $elem.attr('portlet-name');
      var key     = $elem.attr('portlet-key');

      if (!manager || ! name || !key) {
        return '';
      }

      return ({
        'url': window.location.origin + window.location.pathname + '/portlet_deferred_render',
        'data': {
          'manager': manager,
          'name': name,
          'key': key
        }
      });
    }

    function updatePortlet(elem){
      // Returns a funciton to update the portlet represented by elem DOM
      var fn = function(data) {
        var $elem = jq(elem),
            $data = jq(data);

        // We want to be sure we got the portlet and not an error page
        if ($data.hasClass('portlet-deferred')) {
          $data.find('.portletBody').slimScroll({'height': '240px'});
          $elem.replaceWith($data);
        } else {
          $elem.find('.portletBodyWrapper').empty();
        }
      };
      return fn;
    }

    function deferredRender(elem) {
      // Starts the deferred render of the portlet,
      // if it has enough info
      var urlInfo = deferredUrlInfo(elem);
      if (!urlInfo) {
        return;
      }

      var url = urlInfo.url;
      var data = urlInfo.data;

      // Return promise from ajax call
      return jq.get(url, data, updatePortlet(elem));
    }

    var deferredPortlets = jq('.portlet-deferred').map(function(i, elem) {
      return deferredRender(elem);
    });

    // When all promises are complete
    jq.when.apply(jq, deferredPortlets ).then(function(){
      // Exec attachPortletButtons from core js.
      attachPortletButtons();
    });
  }

  // public interface
  return {
        initDeferredPortlets: initDeferredPortlets,
  };
}) ();


// run on load
jq(function() {
  var me = vnc_collab_common;
  me.initDeferredPortlets();
});
