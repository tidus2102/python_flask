

class FlaskAjaxForm(object):
    def __init__(self, app=None):
        self.app = app
        if self.app is not None:
            self.init_app()

    def init_app(self):
        self.app.jinja_env.globals['FlaskAjaxForm'] = self


    def startForm(self, options):
        self.beforeSubmit = options.get('beforeSubmit', 'undefined')
        self.successCallback = options.get('successCallback', 'undefined')
        self.dataType = options.get('dataType', 'json')
        self.id = options.get('id', 'FlaskAjaxForm')

        return """
            <form method="POST"
            class="%(cssClass)s" 
            id="%(id)s" action="%(action)s">

        """ % {
            'cssClass': options.get('cssClass', 'FlaskAjaxForm'),
            'id': self.id,
            'action': options.get('action', '')
        }


    def endForm(self):
        jsScript = """
            <script type="text/javascript">
            $(document).ready(function() {
                $("form#%(formID)s").submit(function() {
                  var $form = $(this);
                  $form.find("input[type=submit]").attr("disabled", "disabled");
                  $form.find(".ajax-loading").show();

                  var beforeSubmit = %(beforeSubmit)s;
                  var successCallback = %(successCallback)s;

                  if (beforeSubmit != undefined) {
                    beforeSubmit();
                  }

                  $form.ajaxSubmit({
                    dataType: '%(dataType)s',
                    success: function(data) {
                      $form.find("input[type=submit]").removeAttr("disabled");
                      $form.find(".ajax-loading").hide();
                      if (!data.success) {
                        $.each(data.errors, function(key, value) {
                          $("#%(formID)s #" + key + "_error").html(value);
                          $("#%(formID)s #" + key + "_error").removeClass('hide');
                        });
                      } else {
                        if (successCallback != undefined) {
                          successCallback(data);
                        }
                      }
                    }
                  });                    
                  return false;
                });
            });
            </script>
        """ % {
            'formID': self.id,
            'dataType': self.dataType,
            'beforeSubmit': self.beforeSubmit,
            'successCallback': self.successCallback
        }

        return "</form> %s " % jsScript



