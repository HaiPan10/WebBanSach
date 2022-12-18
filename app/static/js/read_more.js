void function $getLines($){
    function countLines($element){
        var lines          = 0;
        var greatestOffset = void 0;

        $element.find('character').each(function(){
            if(!greatestOffset || this.offsetTop > greatestOffset){
                greatestOffset = this.offsetTop;
                ++lines;
            }
        });

        return lines;
    }

    $.fn.getLines = function $getLines(){
        var lines = 0;
        var clean = this;
        var dirty = this.clone();

        (function wrapCharacters(fragment){
            var parent = fragment;

            $(fragment).contents().each(function(){
                if(this.nodeType === Node.ELEMENT_NODE){
                    wrapCharacters(this);
                }
                else if(this.nodeType === Node.TEXT_NODE){
                    void function replaceNode(text){
                        var characters = document.createDocumentFragment();

                        text.nodeValue.replace(/[\s\S]/gm, function wrapCharacter(character){
                            characters.appendChild($('<character>' + character + '</>')[0]);
                        });

                        parent.replaceChild(characters, text);
                    }(this);
                }
            });
        }(dirty[0]));

        clean.replaceWith(dirty);

        lines = countLines(dirty);

        dirty.replaceWith(clean);

        return lines;
    };
}(jQuery);

function readMore_des(jObj, lineNum, line_count) {
  if ( line_count > lineNum){
    var go = new ReadMore_des (jObj, lineNum);
  }
}

//class
function ReadMore_des(_jObj, lineNum) {
  $('.hidden-text_des').addClass( "fadeOnHidden" );
  var READ_MORE_LABEL = '...<br>Xem thêm';
  var HIDE_LABEL = 'Thu nhỏ';

  var jObj = _jObj;
  var textMinHeight = ''+ (parseInt(jObj.children('.hidden-text_des').css('line-height'),10)*lineNum) +'px';
  var textMaxHeight = ''+jObj.children('.hidden-text_des').css('height');

  jObj.children('.hidden-text_des').css('height', ''+ textMaxHeight);
  jObj.children('.hidden-text_des').css( 'transition', 'height .5s');
  jObj.children('.hidden-text_des').css('height', ''+ textMinHeight);

  jObj.append ('<button class="read-more_des">'+READ_MORE_LABEL+'</button>');

  jObj.children('.read-more_des').click ( function() {
    if (jObj.children('.hidden-text_des').css('height') === textMinHeight) {
      jObj.children('.hidden-text_des').css('height', ''+textMaxHeight);
      jObj.children('.read-more_des').html(HIDE_LABEL).addClass('active');
      $('.hidden-text_des').removeClass( "fadeOnHidden" )
    } else {
    $('.hidden-text_des').addClass( "fadeOnHidden" )
      jObj.children('.hidden-text_des').css('height', ''+textMinHeight);
      jObj.children('.read-more_des').html(READ_MORE_LABEL).removeClass('active');
    }
  });

}

function readMore_cmt(jObj, lineNum) {
  var go = new ReadMore_cmt (jObj, lineNum);
}

//class
function ReadMore_cmt(_jObj, lineNum) {
  $('.hidden-text_cmt').addClass( "fadeOnHidden" );
  var READ_MORE_LABEL = '...<br>Xem thêm';
  var HIDE_LABEL = 'Thu nhỏ';

  var jObj = _jObj;
  var textMinHeight = ''+ (parseInt(jObj.children('.hidden-text_cmt').css('line-height'),10)*lineNum) +'px';
  var textMaxHeight = ''+jObj.children('.hidden-text_cmt').css('height');

  if(flag_t == 1) { textMaxHeight = '400px'; }

  jObj.children('.hidden-text_cmt').css('height', ''+ textMaxHeight);
  jObj.children('.hidden-text_cmt').css( 'transition', 'height .5s');
  jObj.children('.hidden-text_cmt').css('height', ''+ textMinHeight);

  jObj.append ('<button class="read-more_cmt">'+READ_MORE_LABEL+'</button>');

  jObj.children('.read-more_cmt').click ( function() {
    if (jObj.children('.hidden-text_cmt').css('height') === textMinHeight) {
      jObj.children('.hidden-text_cmt').css('height', ''+textMaxHeight);
      jObj.children('.read-more_cmt').html(HIDE_LABEL).addClass('active');
      $('.hidden-text_cmt').removeClass( "fadeOnHidden" )
    } else {
    $('.hidden-text_cmt').addClass( "fadeOnHidden" )
      jObj.children('.hidden-text_cmt').css('height', ''+textMinHeight);
      jObj.children('.read-more_cmt').html(READ_MORE_LABEL).removeClass('active');
    }
  });

}