exports.parseType = function(parse){
  //var parse = '[S [NP It_PRP NP] [VP enables_VBZ [NP [NP browsing_NN NP] [PP of_IN [NP [NP large_JJ collections_NNS NP] [PP of_IN [NP data_NNS NP] PP] NP] PP] [PP via_IN [NP [NP predefined_JJ sets_NNS NP] [PP of_IN [NP concepts_NNS and_CC relations_NNS NP] PP] [PP among_IN [NP them_PRP NP] PP] NP] PP] NP] VP] ._. S]';
  parse = parse.replace(/[][]/g, ' ');
  var ents = [];
  var NNP = false;
  parse.replace(/([^ ]*)_([a-zA-Z0-9.]+)/g, function(_, token, type) {
      console.log(token, type);
      if (type==="NNP"){//NNP
        if (!NNP){//first NNP
          NNP = true;         
        }else{//second NNP, join
          var last = ents.pop();
        }
        token = '';
      }else if(type==="PRP" || type==="."){
        token='';
      }else {//anything else
        if(NNP) NNP=false;
        if(type==="CD"){
          if (token <0 || token >1 ){
            token = "#";
          }
        }
      }
      ents.push(token.toLowerCase() + '_' + type);
      
  });
  var join = ents.join(' ')
  //console.log(join);
  return join;
}