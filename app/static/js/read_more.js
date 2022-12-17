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

function readMore(jObj, lineNum, line_count) {
console.log(lineNum);
console.log(line_count);
  if ( line_count > lineNum){
    var go = new ReadMore (jObj, lineNum);
  }
}

//class
function ReadMore(_jObj, lineNum) {
  var READ_MORE_LABEL = '...<br>Xem thêm';
  var HIDE_LABEL = 'Thu nhỏ';

  var jObj = _jObj;
  var textMinHeight = ''+ (parseInt(jObj.children('.hidden-text').css('line-height'),10)*lineNum) +'px';
  var textMaxHeight = ''+jObj.children('.hidden-text').css('height');

  jObj.children('.hidden-text').css('height', ''+ textMaxHeight);
  jObj.children('.hidden-text').css( 'transition', 'height .5s');
  jObj.children('.hidden-text').css('height', ''+ textMinHeight);

  jObj.append ('<button class="read-more">'+READ_MORE_LABEL+'</button>');

  jObj.children('.read-more').click ( function() {
    if (jObj.children('.hidden-text').css('height') === textMinHeight) {
      jObj.children('.hidden-text').css('height', ''+textMaxHeight);
      jObj.children('.read-more').html(HIDE_LABEL).addClass('active');
    } else {
      jObj.children('.hidden-text').css('height', ''+textMinHeight);
      jObj.children('.read-more').html(READ_MORE_LABEL).removeClass('active');
    }
  });

}