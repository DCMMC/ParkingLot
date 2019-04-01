/**
 * a 2d Canvas renderer for fast rendering
 * Created by gaimeng on 15/2/2.
 */

//---------------------IndoorMap2D class-----------------
IndoorMap2d = function(mapdiv){
    var _this = this;
    var _mapDiv = mapdiv;
    var _controls;

    var _curFloorId = 0;
    var _selectionListener = null;
    var _selected, _selectedOldColor;
    var _theme = null;

    this.options = {
        showNames : true,
        showPubPoints : true,
        selectable : true,
        movable: true
    }
    this.containerSize = [0, 0];
    this.containerHalfSize = [0, 0];
    this.containerPos = [0,0];
    this.mapCenter = [0 ,0];

    this.renderer = null;
    this.is3d = false;

    //var _marker;

    this.init = function(){
        _this.containerSize[0] = parseInt(_mapDiv.style.width);
        _this.containerSize[1] = parseInt(_mapDiv.style.height);
        _this.containerHalfSize[0] = _this.containerSize[0] / 2;
        _this.containerHalfSize[1] = _this.containerSize[1] / 2;
        _this.containerPos = IDM.DomUtil.getPos(_mapDiv);

        _this.renderer = new Canvas2DRenderer(_this);
        var canvasDiv = _this.renderer.domElement;
        _controls = new Controller2D(_this.renderer);
        _mapDiv.appendChild(canvasDiv);
        _mapDiv.style.overflow = "hidden";


    }

    this.reset = function(){
        _controls.reset();
        _this.renderer.reset();
    }

    this.setTheme = function(theme){
        if(_theme == null){
            _theme = theme
        } else if(_theme != theme) {
            _theme = theme;
            _this.parse(_this.mall.jsonData); //parse
            redraw();
        }
        return _this;
    }

    this.theme = function(){
        return _theme;
    }

    this.getMall = function(){
        return _this.mall;
    }

    //load the map by the json file name
    this.load = function (fileName, callback) {
        _this.reset();
        _theme = default2dTheme;
        var loader = new IndoorMapLoader(false);
        loader.load(fileName, function(mall){
            _this.mall = mall;
            _this.showFloor(_this.mall.getDefaultFloorId());
            if(callback) {
                callback();
            }


        });
    }

    this.parse = function(json){
        _this.reset();
        if(_theme == null) {
            _theme = default2dTheme;
        }
        _this.mall = ParseModel(json, _this.is3d, _theme);
        _this.showFloor(_this.mall.getDefaultFloorId());

        _mapDiv.style.background = _theme.background;
        return _this;
    }

    //reset the camera to default configuration
    this.setDefaultView = function () {
        _this.renderer.setDefaultView(_this.mall.getCurFloor());

        _controls.reset();
        _controls.viewChanged = true;
    }

    //TODO:adjust camera to fit the building
    this.adjustCamera = function() {
        _this.setDefaultView();

    }

    this.translate = function(vec){
        _this.renderer.translate(vec);
    }

    this.zoomIn = function(zoomScale){
        if(zoomScale === undefined){
            zoomScale = 1.25;
        }
        _this.renderer.scale(zoomScale);
    }

    this.zoomOut = function(zoomScale){
        if(zoomScale === undefined){
            zoomScale = 0.8;
        }
        _this.renderer.scale(zoomScale);
    }

    this.showAreaNames = function(show) {
        _this.options.showNames = show == undefined ? true : show;
        redraw();
        return _this;
    }

    //show pubPoints(entries, ATM, escalator...)
    this.showPubPoints = function(show){
        _this.options.showPubPoints = show == undefined ? true: show;
        redraw();
        return _this;
    }

    //get the selected object
    this.getSelectedId = function(){
        var id;
        if(_selected && _selected.BrandShop) {
            id = _selected.BrandShop;
        }else{
            id = -1;
        }
        return id;
    }

    //the callback function when sth is selected
    this.setSelectionListener = function(callback){
        _selectionListener = callback;
        return _this;
    }

    //select object by id
    this.selectById = function(id){
        var floor = _this.mall.getCurFloor();
        for(var i = 0; i < floor.FuncAreas.length; i++){
            if(floor.FuncAreas[i].BrandShop && floor.FuncAreas[i].BrandShop == id) {
                _this.deselectAll();
                _this.select(floor.FuncAreas[i]);
            }
        }
    }

    //show floor by id
    this.showFloor = function(floorid) {
        if(_this.mall == null){
            return;
        }
        _curFloorId = floorid;
        _this.mall.showFloor(floorid);

        if(_this.options.showNames) {
            _this.renderer.createNameTexts(floorid, _this.mall);
        }

        if(_this.options.showPubPoints) {
            _this.renderer.loadSpirtes(_this.mall);
        }

        _this.adjustCamera();

        return _this;
    }

//    this.setSelectionMarker = function(marker){
//        //_marker = marker;
//    }

    //set if the objects are selectable
    this.setSelectable = function (selectable) {
        if(selectable){
            _mapDiv.addEventListener('mouseup', onSelectObject, false);
            _mapDiv.addEventListener('touchend', onSelectObject, false);
        }else{
            _mapDiv.removeEventListener('mouseup', onSelectObject, false);
            _mapDiv.removeEventListener('touchend', onSelectObject, false);
        }
        return _this;
    }

    //set if the user can pan the camera
    this.setMovable = function(movable){
        _controls.enable = movable;
        return _this;
    }

    //focus
    this.focus = function (obj){
        _this.renderer.focus(obj);
    }

    this.deselectAll = function(){
        if (_selected) {
            _selected.fillColor = _selectedOldColor;
            redraw();
        }
    }

    //select object(just hight light it)
    this.select = function(obj){
        if(obj != undefined) {
            //_this.focus(obj);
            _selectedOldColor = obj.fillColor;
            obj.fillColor = _theme.selected;
            //var pos = _this.renderer.localToWorld(obj.Center);
            _selected = obj;
            redraw();

//            _marker.style.left = pos[0] - _marker.width / 2;
//            _marker.style.top = pos[1] - _marker.height / 2;
//            _marker.style.visibility = true;
        }
    }

    function onSelectObject(event){
        event.preventDefault();
        var pos = [0,0]
        if(event.type == "touchend"){
            pos[0] = event.changedTouches[0].clientX;
            pos[1] = event.changedTouches[0].clientY;
        }else {
            pos[0] = event.clientX;
            pos[1] = event.clientY;
        }

        if(Math.abs(pos[0] - _controls.startPoint[0] + pos[1] - _controls.startPoint[1]) <5) {
            //turn browser point into container viewport point
            pos[0] -= IDM.DomUtil.getElementLeft(_mapDiv);
            pos[1] -= IDM.DomUtil.getElementTop(_mapDiv);

            //deselect the old one
            _this.deselectAll();

            _selected = _this.renderer.onSelect(pos);

            if (_selected) {
                _this.select(_selected)
                console.log(_this.getSelectedId());
                if (_selectionListener) {
                    _selectionListener(_this.getSelectedId());
                }

            } else {
                if (_selectionListener) {
                    _selectionListener(-1);
                }
            }

        }
        redraw();
    }

    function redraw(){
        _this.renderer.clearBg();
        _this.renderer.render(_this.mall);
    }

    function animate () {
        requestAnimationFrame(animate);
        //_controls.update();
        if(_controls.viewChanged) {
            _this.renderer.render(_this.mall);
            _controls.viewChanged = false;
        }


    }

    _this.init();
    animate();
}

//---------------------the Sprite class------------------
function CanvasSprite(params){
    var _this = this,
        _ctx = params.ctx,
        _width = params.width,
        _height = params.height,
        _offsetX = 0,
        _offsetY = 0,
        _visible = true,

        _img = new Image();
    _img.src = params.image;

    this.draw = function(x, y){
        if(_visible){
            _ctx.drawImage(_img,_offsetX, _offsetY, _width, _height, x >> 0, y >> 0, _width, _height);
        }
    }

    this.show = function(){
        _visible = true;
    }

    this.hide = function(){
        _visible = false;
    }
}

Canvas2DRenderer = function (map) {

    var _this = this,
        _map = map,
        _ctx;
    var _canvas = document.createElement('canvas');

    var _padding = 0.2;  //padding between map bounding box and the div boundary

    var _floorSize = [0, 0];

    //canvas real size
    var _canvasPos = [0, 0], //in the browser coordinate
        _canvasSize = [0, 0],
        _canvasHalfSize = [0, 0],
        _bounds = null,

        _nameTexts = [],
        _sprites = [],
        _pubPoints = [0,0],


        _scale = 1.0;
    var _curFloor = null;
    var _objSize = [0,0];
    var _translate = [0,0];

    this.domElement = _canvas;
    this.mapCenter = [];
    var _devicePixelRatio = 1;

    function _init(){
        _canvas.style.position = "absolute";
        _ctx = _canvas.getContext('2d');
        _this.updateViewport();


    }

    this.updateViewport = function(isZoom){
        var clippadding = clipPadding();
        var clipSize = [(_map.containerSize[0]*clippadding) >> 0, (_map.containerSize[1]*clippadding) >> 0];
        _canvasPos[0] = _map.containerPos[0] - clipSize[0];
        _canvasPos[1] = _map.containerPos[1] - clipSize[1];
        var realRatio = 1 + 2*clippadding;
        _canvasSize[0] = (realRatio * _map.containerSize[0]) >> 0;
        _canvasSize[1] = (realRatio * _map.containerSize[1]) >> 0;
        _canvasHalfSize[0] = _canvasSize[0]*.5;
        _canvasHalfSize[1] = _canvasSize[1]*.5;
        _bounds = new Rect(-_canvasHalfSize[0],-_canvasHalfSize[1],_canvasHalfSize[0], _canvasHalfSize[1]);
        _canvasPos[0] = -clipSize[0]
        _canvasPos[1] = -clipSize[1]
        IDM.DomUtil.setPos(_canvas, _canvasPos);
        _devicePixelRatio = window.devicePixelRatio || 1;
        var area = _canvasSize[0]*_canvasSize[1]*_devicePixelRatio*_devicePixelRatio;
        _devicePixelRatio = (IDM.Browser.mobile && !IDM.Browser.android || IDM.Browser.android23) && (area > 5E6) ? 1 : _devicePixelRatio;
        _canvas.width = _canvasSize[0] * _devicePixelRatio;
        _canvas.height = _canvasSize[1] * _devicePixelRatio;
        _canvas.style.width = _canvasSize[0] + "px";
        _canvas.style.height = _canvasSize[1] + "px";
        _ctx.scale(_devicePixelRatio, _devicePixelRatio);
        _ctx.translate(_canvasHalfSize[0], _canvasHalfSize[1]);
        if(isZoom){
            _ctx.translate(_translate[0],_translate[1]);
        }
    }

    function clipPadding(){
        var ratio = ((IDM.Browser.mobile ? 1280 : 2000) / Math.max(window.innerWidth, window.innerHeight) - 1) / 2;
        return Math.max(0, Math.min(.5, ratio));
    }

    this.translate = function(vec){
        //TODO: clip polygons if necessary

        _translate[0] += vec[0];
        _translate[1] += vec[1];
        _ctx.translate(_translate[0], _translate[1]);
        _this.clearBg();
        _this.render();
    }

    this.scale = function(scale){
        _scale *= scale;
        _curFloor = _map.mall.getCurFloor();
        updateOutline(_curFloor, _scale);
        var funcAreas = _curFloor.FuncAreas;
        for(var i = 0; i < funcAreas.length; i++){
            updateOutline(funcAreas[i], _scale);
        }
        var pubPoints = _curFloor.PubPoint;
        for(var i = 0; i < pubPoints.length ; i++){
            updateOutline(pubPoints[i], _scale);
        }
        _ctx.translate(-_translate[0], -_translate[1]);
        _translate[0] *= scale;
        _translate[1] *= scale;
        _ctx.translate(_translate[0], _translate[1]);
        _this.clearBg();
        _this.render();
    }
    function updateOutline(obj, scale){
        var outline = obj.Outline[0][0];
        obj.newOutline = [];
        for(var i = 0; i < outline.length - 1; i+=2){
            var newPoint = updatePoint([outline[i], outline[i+1]], scale);
            obj.newOutline.push(newPoint[0]);
            obj.newOutline.push(newPoint[1]);
        }
        obj.rect = IDM.GeomUtil.getBoundingRect(obj.newOutline);
        //if(!obj.rect.isCollide(_bounds)){
        //    obj.newOutline = [];
        //    obj.rect = new Rect();
        //}
        if(obj.Center) {
            obj.Center = [((obj.rect.br[0]+obj.rect.tl[0])/2) >> 0 , ((obj.rect.br[1]+obj.rect.tl[1])/2) >> 0];
        }
    }

    function updatePoint(point, scale){
        return [((point[0] - _this.mapCenter[0])*scale)>>0, ((point[1] - _this.mapCenter[1])*scale)>>0];
    }

    this.setDefaultView = function (floor) {
        floor.rect = IDM.GeomUtil.getBoundingRect(floor.Outline[0][0]);

        var floorSize = [0, 0];
        floorSize[0] = floor.rect.br[0] - floor.rect.tl[0];
        floorSize[1] = floor.rect.br[1] - floor.rect.tl[1];
        var scaleX = (_map.containerSize[0]*(1 - _padding)) / floorSize[0];
        var scaleY = (_map.containerSize[1]*(1 - _padding)) / floorSize[1];


        _this.mapCenter[0] = (floor.rect.br[0] + floor.rect.tl[0]) / 2;
        _this.mapCenter[1] = (floor.rect.br[1] + floor.rect.tl[1]) / 2;

        _ctx.translate(-_translate[0], -_translate[1]);
        _scale = 1.0;
        _translate = [0, 0];
        _this.scale(Math.min(scaleX , scaleY));
    }

    this.reset = function(){
        _nameTexts.length = 0;


    }

    this.focus = function (object) {
        //if(object._id != _oldId) {

        var width = object.rect.br[0] - object.rect.tl[0];
        var height = object.rect.br[1] - object.rect.tl[1];
        var floor = _map.getMall().getCurFloor();
        var floorSize = [0, 0];
        floorSize[0] = floor.rect.br[0] - floor.rect.tl[0];
        floorSize[1] = floor.rect.br[1] - floor.rect.tl[1];
        var ratio = (width+height) / (floorSize[0]+floorSize[1]);
        //var padding = ratio > 0.005? _mapWidth * 0.5 : _mapWidth * 0.85;


        var minSize = Math.min(_map.containerSize[0], _map.containerSize[1]);
        var padding = (-1.42*ratio + 0.9) * minSize; //empirical value
        minSize /= 2;
        padding < minSize? padding = minSize : padding;
        var scaleX = (_map.containerSize[0] - padding) / width;
        var scaleY = (_map.containerSize[1] - padding) / height;
        _objSize[0] = width;
        _objSize[1] = height;
        var tmpScale = scaleX < scaleY ? scaleX : scaleY;
        _this.scale(tmpScale);

        var center = [];
        center[0] = (object.rect.br[0] + object.rect.tl[0]) / 2;
        center[1] = - (object.rect.br[1] + object.rect.tl[1]) / 2;
        var curCenter = _this.worldToLocal([_map.containerHalfSize[0], _map.containerHalfSize[1]]);
        var vec = [curCenter[0]-center[0], curCenter[1]-center[1]];
        _this.updateViewport();
        _this.translate(vec);
    }

    this.screenShot = function(type){
        var tmpCanvas = document.createElement("canvas");
        tmpCanvas.width = _map.containerSize[0], tmpCanvas.height = _map.containerSize[1];

        var tmpCtx = tmpCanvas.getContext('2d');
        tmpCtx.drawImage(_canvas,_canvasPos[0],_canvasPos[1]);
        return tmpCanvas.toDataURL(type);
    }

    this.render = function (){
        if(_map.mall === undefined) {
            return;
        }

        var theme = _map.theme();

        //get render data
        _curFloor = _map.mall.getCurFloor();

        _ctx.save();

        //draw floor
        var poly = _curFloor.newOutline;
        _ctx.beginPath();
        _ctx.moveTo(poly[0], -poly[1]);
        for(var i = 2; i < poly.length - 1; i+=2){
            _ctx.lineTo(poly[i],-poly[i+1]);
        }
        _ctx.closePath();

        _ctx.fillStyle = _curFloor.fillColor;
        _ctx.fill();
        _ctx.strokeStyle = theme.strokeStyle.color;
        _ctx.lineWidth = theme.strokeStyle.linewidth;
        _ctx.stroke();

        //draw funcAreas
        var funcAreas = _curFloor.FuncAreas;
        for(var i = 0 ; i < funcAreas.length; i++){
            var funcArea = funcAreas[i];
            var poly = funcArea.newOutline;
            if(poly.length < 6){ //less than 3 points, return
                continue;
            }
            _ctx.beginPath();

            _ctx.moveTo(poly[0], -poly[1]);
            for(var j = 2; j < poly.length - 1; j+=2){
                _ctx.lineTo(poly[j],-poly[j+1]);
            }
            _ctx.closePath();

            _ctx.fillStyle = funcArea.fillColor;
            _ctx.fill();
            _ctx.stroke();
        }

        ////test for selection
        //_ctx.fillStyle="#FF0000";
        //_ctx.beginPath();
        //_ctx.arc(_pubPoints[0],_pubPoints[1],5,0,Math.PI*2,true);
        //_ctx.closePath();
        //_ctx.fill();

        _ctx.restore();

        var options = _map.options;
        if(options.showNames){
            var fontStyle = theme.fontStyle;
            //_ctx.textAlign = fontStyle.textAlign;
            _ctx.textBaseline = fontStyle.textBaseline;
            _ctx.fillStyle = theme.fontStyle.color;
            _ctx.font =  fontStyle.fontsize + "px/1.4 " + fontStyle.fontface;
            var textRects = [];
            for(var i = 0 ; i < funcAreas.length; i++){
                var nameText = _nameTexts[i];

                var center = funcAreas[i].Center;

                var rect = new Rect(center[0] - nameText.halfWidth, -center[1] - nameText.halfHeight, center[0] + nameText.halfWidth, -center[1] + nameText.halfHeight);
                textRects.push(rect);

                nameText.visible = true;

                //for(var j = 0; j < i; j++){
                //    if(_nameTexts[j].visible && textRects[j].isCollide(rect)){
                //        nameText.visible = false;
                //        break;
                //    }
                //}
                if((funcAreas[i].rect.br[0]-funcAreas[i].rect.tl[0])*0.9 < nameText.halfWidth*2)
                    nameText.visible = false;
                if(nameText.visible) {
                    _ctx.fillText(nameText.text, (center[0] - nameText.halfWidth) >> 0, (-center[1]) >> 0);
//                _ctx.beginPath();
//                _ctx.arc(center[0], center[1], 3, 0, Math.PI * 2, true);
//                _ctx.closePath();
//
//                _ctx.fill();
//                    _ctx.strokeRect(rect.tl[0], rect.tl[1], rect.br[0] - rect.tl[0], rect.br[1] - rect.tl[1]);
                }
            }
        }

        if(options.showPubPoints){
            var pubPoints = _curFloor.PubPoint;
            var imgWidth = 20 , imgHeight = 20 ;
//            if(_scale < 0.1){
//                imgWidth = imgHeight = 12;
//            }

            var imgWidthHalf = imgWidth/2, imgHeightHalf = imgHeight/2;
            var pubPointRects = [];
            for(var i = 0; i < pubPoints.length; i++){
                var pubPoint = pubPoints[i];
                var center = pubPoint.newOutline;
                var rect = new Rect(center[0] - imgWidthHalf, -center[1] - imgHeightHalf, center[0] + imgWidthHalf, -center[1] + imgHeightHalf);
                pubPointRects.push(rect);

                pubPoint.visible = true;
                for(var j = 0; j < i; j++){
                    if(pubPoints[j].visible && pubPointRects[j].isCollide(rect)){
                        pubPoint.visible = false;
                        break;
                    }
                }
                if(pubPoint.visible) {
                    var image = _sprites[pubPoints[i].Type];
                    if (image !== undefined) {
                        _ctx.drawImage(image, (center[0] - imgWidthHalf) >> 0, (-center[1] - imgHeightHalf) >> 0, imgWidth, imgHeight);
                    }
                }
            }
        }

    }

    //map the coordinate in the map to the viewport
    //!!hasnt been tested yet
    this.localToWorld = function(pt){
        var worldPoint = [0,0];
        worldPoint[0] = pt[0]+_translate[0]+_map.containerHalfSize[0] >> 0;
        worldPoint[1] = pt[1]+_translate[1]+_map.containerHalfSize[1] >> 0;
        return worldPoint;
    }

    //map the coordinate in the viewport to the map (with -y)
    this.worldToLocal = function(pt){
        var localPoint = [0,0];
        localPoint[0] = (pt[0]-_translate[0]-_map.containerHalfSize[0]) >> 0;
        localPoint[1] = (pt[1]-_translate[1]-_map.containerHalfSize[1]) >> 0;
        return localPoint;
    }

    this.onSelect = function(point){
        var tmpPos = _this.worldToLocal(point);
        //_pubPoints = tmpPos;
        return hitTest(tmpPos);
    }

    this.setSize = function(width, height) {
        _canvas.style.width = width + "px";
        _canvas.style.height = height + "px";
        _canvasSize[0] = width * _devicePixelRatio;
        _canvasSize[1] = height * _devicePixelRatio;
        _canvas.width = _canvasSize[0];
        _canvas.height = _canvasSize[1];
        _canvasHalfSize[0] = Math.floor(width / 2);
        _canvasHalfSize[1] = Math.floor(height / 2);
        _ctx.scale(_devicePixelRatio, _devicePixelRatio);
    }

    function exceed(scale){
        //var curWidth = _objSize[0] * scale;
        //var curHeight = _objSize[1] * scale;
        //var maxSize = MAX_CANVAS_SIZE * _devicePixelRatio;
        //if(curWidth > maxSize || curHeight > maxSize){
        //    return true;
        //}else{
        //    return false;
        //}
        return false;
    }

    this.clearBg = function(){
        //clear background
        _ctx.save();
        _ctx.setTransform(1,0,0,1,0,0);
        _ctx.fillStyle = _map.theme().background;
        _ctx.fillRect(0,0,_canvasSize[0]*_devicePixelRatio, _canvasSize[1]*_devicePixelRatio);
        _ctx.restore();
    }

    function hitTest(point){
        _ctx.save();
        _ctx.setTransform(1,0,0,1,0,0);
        for(var i = 0 ; i < _curFloor.FuncAreas.length; i++) {
            var funcArea = _curFloor.FuncAreas[i];
            if((!funcArea.Category) && parseInt(funcArea.Type) == 100){ //hollow area
                continue;
            }

            var rect = funcArea.rect;
            if((point[0]<rect.tl[0] && point[0] < -rect.br[1]) || (point[0]>rect.br[0] && point[0] > -rect.tl[1]))
                continue;

            var poly = funcArea.newOutline;
            if (poly.length < 6) { //less than 3 points, return
                continue;
            }
            _ctx.beginPath();

            _ctx.moveTo(poly[0], -poly[1]);
            for (var j = 2; j < poly.length - 1; j += 2) {
                _ctx.lineTo(poly[j], -poly[j + 1]);
            }
            _ctx.closePath();

            if (_ctx.isPointInPath(point[0], point[1])) {
                _ctx.restore();
                return funcArea;
            }
        }

        _ctx.restore();
        return null;
    }

    this.loadSpirtes = function(mall){
        if(mall != null && _sprites.length == 0 ){
            var images = _map.theme().pubPointImg;
            for( var key in images){
                var loader = new THREE.ImageLoader();

                var image = loader.load( images[key], function(image){
                    _this.render(mall);
                })

                _sprites[key] = image;
            }
        }
        _sprites.isLoaded = true;
    }

    this.createNameTexts = function(floorId, mall){
        if(_nameTexts.length != 0){
            _nameTexts.length = 0;
        }
        var funcAreaJson = mall.getFloorJson(mall.getCurFloorId()).FuncAreas;
        var fontStyle = _map.theme().fontStyle;
        _ctx.font =  fontStyle.fontsize + "px/1.4 " + fontStyle.fontface;
        for(var i = 0 ; i < funcAreaJson.length; i++){
            var name = {};
            var funcArea = funcAreaJson[i];
            if((!funcArea.Category) && ((parseInt(funcArea.Type) == 100) || (parseInt(funcArea.Type) == 300))){
                name.text = "";
                name.halfWidth = 0;
                name.halfHeight = 0;
                name.visible = false;
            }else {
                name.text = funcAreaJson[i].Name;
                name.halfWidth = _ctx.measureText(name.text).width / 2;
                name.halfHeight = fontStyle.fontsize  / 4;
                name.visible = true;
            }

            _nameTexts.push(name);
        }
    }

    _init();
}

//---------------------Controller2D class-----------------

Controller2D = function(renderer){
    var _renderer = renderer;
    var domElement = _renderer.domElement;
    this.domElement = ( domElement !== undefined ) ? domElement : document;
    this.viewChanged = true;
    this.enable = true;

    var _startPos = [];
    var _curPos = [];

    var _this = this;

    this.startPoint = [0, 0];
    this.endPoint = [0, 0];
    var _panVector = [0, 0];
    var _zoomDistStart = 0, _zoomDistEnd = 0;
    var _zoomScale = 1;
    var STATE = {NONE: -1, ZOOM: 1, PAN: 2}
    var _state = STATE.NONE;

    this.reset = function(){
        _this.startPoint = [0,0];
        _this.endPoint = [0,0];
    }

    this.translate = function(){
        _curPos[0] = (_startPos[0] + _panVector[0]);
        _curPos[1] = (_startPos[1] + _panVector[1]);
        IDM.DomUtil.setPos(domElement, [_curPos[0], _curPos[1]]);
    }

    this.zoom = function(){
        var pos = IDM.DomUtil.getPos(domElement);
        domElement.style[IDM.DomUtil.TRANSFORM] = IDM.DomUtil.getTranslateString(pos) + " scale(" + _zoomScale + ") ";
    }

    function touchStart(event){

        event.preventDefault();

        var touches = event.touches;
        if(touches.length == 1){ //pan
            _this.startPoint[0] = touches[0].clientX;
            _this.startPoint[1] = touches[0].clientY;
            var point = IDM.DomUtil.getPos(domElement);
            _startPos[0] = point[0];
            _startPos[1] = point[1];

        }
        else if( touches.length == 2){ //zoom
            var dx = touches[1].clientX - touches[0].clientX;
            var dy = touches[1].clientY - touches[0].clientY;
            _zoomDistEnd = _zoomDistStart = Math.sqrt( dx * dx + dy * dy );


        }
        else{
            _state = STATE.NONE;
            return;
        }
        if(_this.enable === false) return;

        document.addEventListener('touchend', touchEnd, false);
        document.addEventListener('touchmove', touchMove, false);


    }

    function mouseDown(event){

        event.preventDefault();
        _this.startPoint[0] = event.clientX;
        _this.startPoint[1] = event.clientY;

        if(_this.enable === false) return;

        document.addEventListener('mouseup', mouseUp, false);
        document.addEventListener('mousemove', mouseMove, false);

        var point = IDM.DomUtil.getPos(domElement);
        _startPos[0] = point[0];
        _startPos[1] = point[1];



    }

    function touchMove(event){
        if(_this.enable === false) return;
        event.preventDefault();
        event.stopPropagation();

        var touches = event.touches;
        if(touches.length == 1) {
            _this.endPoint[0] = touches[0].clientX;
            _this.endPoint[1] = touches[0].clientY;

            _panVector = [_this.endPoint[0]-_this.startPoint[0], _this.endPoint[1]-_this.startPoint[1]];
            _this.translate();
            _state = STATE.PAN;

        }else if( touches.length == 2){
            var dx = touches[1].clientX - touches[0].clientX;
            var dy = touches[1].clientY - touches[0].clientY;
            _zoomDistEnd = Math.sqrt( dx * dx + dy * dy );
            _zoomScale = _zoomDistEnd / _zoomDistStart;
            _this.zoom( );
            _state = STATE.ZOOM;
        }
    }

    function mouseMove(event){
        if(_this.enable === false) return;
        event.preventDefault();
        event.stopPropagation();

        _this.endPoint[0] = event.clientX;
        _this.endPoint[1] = event.clientY;

        _panVector = [_this.endPoint[0] - _this.startPoint[0], _this.endPoint[1] - _this.startPoint[1]];

        if(event.button === 0) {


            _this.translate();
            _state = STATE.PAN;
        }
        else if(event.button === 1){

            _zoomScale = (Math.abs(_panVector[0])+Math.abs(_panVector[1]))/1000;
            if(_panVector[1] < 0){
                _zoomScale = -_zoomScale;
            }
            _zoomScale += 1;
            _this.zoom( );
            _state = STATE.ZOOM;
        }

    }

    function mouseWheel(event){
        if(_this.enable === false) return;
        var delta = 0;
        delta = event.wheelDelta ? (event.wheelDelta / 120) : (- event.detail / 3);
        delta > 0 ? delta *= 1.25 : delta *= -0.8;
        _renderer.scale(delta);
    }

    function touchEnd(event){
        if(_this.enable === false) return;
        if(_state == STATE.PAN) {
            panEnd();
        }else if(_state == STATE.ZOOM) {
            zoomEnd();
        }
        _state = STATE.NONE;
        document.removeEventListener('touchend', touchEnd, false);
        document.removeEventListener('touchmove', touchMove, false);
    }

    function mouseUp(event){
        if(_this.enable === false) return;
        if(_state == STATE.PAN) {
            panEnd();
        }else if(_state == STATE.ZOOM) {
            zoomEnd();
        }
        _state = STATE.NONE;
        document.removeEventListener('mouseup', mouseUp, false);
        document.removeEventListener('mousemove', mouseMove, false);
    }

    function panEnd(){
        if(Math.abs(_panVector[0]+_panVector[1]) < 5) return;

        _renderer.updateViewport();
        _renderer.translate(_panVector);
    }

    function zoomEnd(){
        _renderer.updateViewport(true);
        _renderer.scale(_zoomScale);
    }

    this.domElement.addEventListener('touchstart', touchStart, false);
    this.domElement.addEventListener('mousedown', mouseDown, false);
    this.domElement.addEventListener('mousewheel', mouseWheel,false);


}