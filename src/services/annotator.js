export default {}

// Iris annotator javascript.
// Based on Oliveira's Image Markup project.
// Ref: https://www.codeproject.com/Articles/801111/Html-Image-Markup.

// // Generates a UUID for javascript objects.
// let generateUUID = function () {
//     let d = new Date().getTime();
//     let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
//         let r = (d + Math.random() * 16) % 16 | 0;
//         d = Math.floor(d / 16);
//         return (c === 'x' ? r : (r & 0x7 | 0x8)).toString(16);
//     });
//     return uuid;
// };

// // Iris annotator code.
// (function ($) {
//     // annotation defaults (color, line width, opacity)
//     let defaults = {
//         opacity: .5,
//         match_color: 'green',
//         non_match_color: 'red',
//         patch_width: 4,
//         link_width: 2,
//         delete_key: 'backspace'
//     };

//     // control/status attributes
//     let currentPatch;
//     let selectedItem = null;
//     let linkSource = null;
//     let linkSources = [];
//     let linkTargets = [];
//     let links = [];
//     let contextPoint;
//     let canvasWidth;

//     // iris-annotator details
//     $.fn.irisAnnotator = function (options) {
//         // settings, self reference, option setup...
//         let settings = $.extend({}, defaults, options || {});
//         let self = this;
//         this.setOptions = function (options) {
//             settings = $.extend(settings, options);
//         };

//         // JSON server side save, on submit
//         window.onsubmit = function () {
//             document.getElementById('annot_json_id').value = paper.projects[0].exportJSON();
//         };

//         // loading code
//         window.onload = function () {
//             $(self).each(function (eachIndex, eachItem) {
//                 self.paths = [];

//                 let img = eachItem;
//                 let canvas = $('<canvas>')
//                     .attr({
//                         width: $(img).width(),
//                         height: $(img).height() - 4
//                     })
//                     .addClass('iris-canvas')
//                     .css({
//                         left: '50%',
//                         position: 'absolute',
//                         transform: 'translateX(-50%)'
//                     });

//                 canvasWidth = $(img).width();

//                 $(img).after(canvas);
//                 $(img).data('paths', []);

//                 paper.setup(canvas[0]);
//                 $(canvas).mouseenter(function () {
//                     paper.projects[eachIndex].activate();
//                 });

//                 // drawing tool
//                 let tool = new paper.Tool();

//                 tool.onMouseMove = function (event) {
//                     // works only if the context menu is not visible
//                     if (!$('.context-menu-list').is(':visible')) {
//                         if (event.item) {
//                             event.item.selected = true;
//                             selectedItem = event.item;
//                             self.setSelectCursor();
//                         } else {
//                             if (selectedItem !== null)
//                                 selectedItem.selected = false;

//                             selectedItem = null;
//                             self.setAnnotateCursor();
//                         }
//                     }

//                     // else, does nothing
//                     paper.view.draw();
//                 };

//                 tool.onMouseDown = function (event) {
//                     switch (event.event.button) {
//                         // left click
//                         case 0:
//                             // if there is not a selected item and there is a current patch
//                             if (!selectedItem && !currentPatch) {
//                                 currentPatch = new paper.Path();
//                                 currentPatch.data.id = generateUUID();
//                                 currentPatch.strokeWidth = settings.patch_width;
//                                 currentPatch.opacity = settings.opacity;

//                                 if (self.getAnnotationType() === 1)
//                                     currentPatch.strokeColor = settings.match_color;
//                                 else
//                                     currentPatch.strokeColor = settings.non_match_color;
//                             }

//                             // else, does nothing
//                             break;

//                         // right click
//                         case 2:
//                             break;
//                     }

//                     paper.view.draw();
//                 };

//                 tool.onMouseDrag = function (event) {
//                     switch (event.event.button) {
//                         // left click
//                         case 0:
//                             // adds a new control point to the current patch
//                             if (currentPatch)
//                                 currentPatch.add(event.point);

//                             break;

//                         // right click
//                         case 2:
//                             break;
//                     }

//                     paper.view.draw();
//                 };

//                 tool.onMouseUp = function (event) {
//                     switch (event.event.button) {
//                         // left click
//                         case 0:
//                             // if there is not a selected item and there is a current patch
//                             if (!selectedItem && currentPatch) {
//                                 // closes and simplifies the current patch
//                                 currentPatch.closed = true;
//                                 currentPatch.simplify();

//                                 // if there is not a link source yet
//                                 if (linkSource === null) {
//                                     // sets the current patch as the link source
//                                     linkSource = currentPatch;
//                                 }

//                                 // else, if the current patch and the
//                                 // link source are on opposite irises,
//                                 // and they are of same nature (match and match,
//                                 // or non-match and non-match), and they both have
//                                 // enough area
//                                 else if (self.differentIrises(linkSource.position, currentPatch.position) &&
//                                     ((self.isNonMatch(currentPatch) && self.isNonMatch(linkSource)) ||
//                                         (!self.isNonMatch(currentPatch) && !self.isNonMatch(linkSource)))) {
//                                     // connects them
//                                     let link = new paper.Path();
//                                     link.data.id = generateUUID();
//                                     link.strokeColor = currentPatch.strokeColor;
//                                     link.strokeWidth = settings.link_width;
//                                     link.opacity = settings.opacity;
//                                     link.add(linkSource.position);
//                                     link.add(currentPatch.position);
//                                     link.simplify();

//                                     linkSources.push(linkSource);
//                                     linkTargets.push(currentPatch);
//                                     links.push(link);

//                                     linkSource.fillColor = currentPatch.strokeColor;
//                                     currentPatch.fillColor = currentPatch.strokeColor;

//                                     linkSource = null;
//                                 }

//                                 // else, they are on the same iris,
//                                 // or they are of different nature (match and non-match)
//                                 else {
//                                     // removes the old link source,
//                                     // and sets the current patch as the new one
//                                     linkSource.remove();
//                                     linkSource = currentPatch;
//                                 }

//                                 // forgets the current patch
//                                 currentPatch = null;
//                             }

//                             // else, does nothing
//                             break;

//                         // right click
//                         case 2:
//                             contextPoint = event.point;
//                             break;
//                     }

//                     paper.view.draw();
//                 };

//                 // draws everything
//                 paper.view.draw();
//             });
//         };

//         // verifies if two patches are over different irises
//         this.differentIrises = function (position1, position2) {
//             ref = canvasWidth / 2.0;

//             if (position1.x < ref && position2.x > ref)
//                 return true;

//             if (position1.x > ref && position2.x < ref)
//                 return true;

//             return false;
//         };

//         // verifies if a given patch is already linked to another one
//         this.isLinked = function (patch) {
//             for (i = 0; i < linkSources.length; i++)
//                 if (linkSources[i].id === patch.id)
//                     return i;

//             for (i = 0; i < linkTargets.length; i++)
//                 if (linkTargets[i].id === patch.id)
//                     return i;

//             for (i = 0; i < links.length; i++)
//                 if (links[i].id === patch.id)
//                     return i;

//             return -1;
//         };

//         // verifies is a given patch is a non-match, based on the color
//         this.isNonMatch = function (patch) {
//             let compare = new paper.Path();
//             compare.strokeColor = settings.non_match_color;

//             if (patch.strokeColor.red === compare.strokeColor.red &&
//                 patch.strokeColor.green === compare.strokeColor.green &&
//                 patch.strokeColor.blue === compare.strokeColor.blue) {
//                 compare.remove();
//                 return true;
//             }

//             compare.remove();
//             return false;
//         };

//         // sets the current cursor as the annotating one
//         this.setAnnotateCursor = function () {
//             let toggle = document.getElementsByName("annotype")[0];
//             if (toggle.checked)
//                 $('.iris-canvas').css('cursor', "url(../imgs/annotate_cursor_non_match.png) 14 50, auto");
//             else
//                 $('.iris-canvas').css('cursor', "url(../imgs/annotate_cursor_match.png) 14 50, auto");
//         };

//         // sets the current cursor as the selecting one
//         this.setSelectCursor = function () {
//             $('.iris-canvas').css('cursor', "url(../imgs/select_cursor.png) 25 25, auto");
//         };

//         // gets the annotation type toggle button choice
//         this.getAnnotationType = function () {
//             let toggle = document.getElementsByName('annotype')[0];
//             if (toggle.checked)
//                 return 2;
//             else
//                 return 1;
//         };

//         // remove option
//         this.remove = function () {
//             // if there is a selected item
//             if (selectedItem) {
//                 // if the selected item is linked,
//                 // cascade deletion
//                 lnk = self.isLinked(selectedItem);
//                 if (lnk > -1) {
//                     links[lnk].remove();
//                     linkSources[lnk].remove();
//                     linkTargets[lnk].remove();

//                     linkSources.splice(lnk, 1);
//                     linkTargets.splice(lnk, 1);
//                     links.splice(lnk, 1);
//                 }

//                 // deletes the selected item
//                 selectedItem.remove();
//             }
//         };

//         // context menu, with remove option only
//         $.contextMenu({
//             selector: '.iris-canvas',
//             callback: function (key, options) {
//                 switch (key) {
//                     case 'remove':
//                         self.remove();
//                         break;
//                 }
//             },
//             items: {
//                 "remove": { name: "Remove", icon: "erase" }
//             }
//         });
//     };
// }(jQuery));
