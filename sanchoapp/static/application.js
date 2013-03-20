    
    var Hermes = {

        init : function( settings ) 
        {
          Hermes.config = {
            urlBase : "/book/api/dictionary/"
          };
          $.extend( Hermes.config, settings );
        },

        define : function(word, paragraph) 
        {
            if (word)
            {
                var url = Hermes.buildUrl(word);        
                $.getJSON( url, function(data) {  
                    Hermes.showResults(word, paragraph, data); 
                });
            }
            else
            {
              paragraph.popover("hide");
            }
        },

        buildUrl : function(word) 
        {
          word = Hermes.stripPunctuation(word);
          word = encodeURIComponent(word);
          return Hermes.config.urlBase + word;
        },

        stripPunctuation : function(word)
        {
            return word.replace("/[\.,-\/#!$%\^&\*;:{}=\-_`~()]/g", "");
        },

        showResults : function(word, paragraph, data) 
        {
            paragraph.popover("destroy");
            paragraph.popover({ title: "<strong>" + word + "</strong>", 
                                html: true, 
                                content: Hermes.buildContent(data)
            });
            paragraph.popover("show");

        },

        buildContent : function(json) 
        {
            var definitions = json['definitions'];
            var html = "<strong>Definition</strong>";
            html += "<ul>";
            for (var i = 0; i < definitions.length; i++) {
                var definition = definitions[i];
                 html += "<li>" + definition.text + "</li>";
            }
            if (definitions.length == 0)
                html += "<li><em>Not found</em></li>";
            html += "</ul>";

            return html;
        }
    };

    $( document ).ready( Hermes.init );
