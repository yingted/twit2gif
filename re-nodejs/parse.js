<<<<<<< HEAD
var test = [];
console.log(typeof test[0]);
=======
var parse = '[S [NP It_PRP NP] [VP enables_VBZ [NP [NP browsing_NN NP] [PP of_IN [NP [NP large_JJ collections_NNS NP] [PP of_IN [NP data_NNS NP] PP] NP] PP] [PP via_IN [NP [NP predefined_JJ sets_NNS NP] [PP of_IN [NP concepts_NNS and_CC relations_NNS NP] PP] [PP among_IN [NP them_PRP NP] PP] NP] PP] NP] VP] ._. S]';
parse = parse.replace(/[][]/g, ' ');
var ents = [];
parse.replace(/([^ ]*)_([a-zA-Z0-9.]+)/g, function(_, token, type) {
    console.log(token, type);
    ents.push(token + '_' + type);
});
console.log(ents.join(' '));
>>>>>>> 49f62f224d7a5ac7b77f6a95b38cc78d7d86622d
