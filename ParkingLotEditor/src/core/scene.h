/****************************************************************************
** Scene
** @brief: manage the scene. provide interface to modify the mapEntities.
** @author: gaimeng
** @date: Dec, 2014
**
****************************************************************************/
#ifndef SCENE_H
#define SCENE_H

#include <QGraphicsScene>

class Feature;
class Building;
class Floor;
class Room;
class PubPoint;
class ImageLayer;
class PolygonFeature;
QT_FORWARD_DECLARE_CLASS(QGraphicsSceneMouseEvent)

enum DATA_TYPE{
    BUILDING,
    FLOOR,
    FUNCAREA,
    PUBPOINT,
    NONE
};

class Scene : public QGraphicsScene
{
    Q_OBJECT
public:
    Building *m_building;
    bool m_selectable = true;
    explicit Scene(QObject *parent = 0);
    void reset();
    void setSelectable(bool b);
    Feature* root() const;
    void createRoot();
    Building* building() const;
    void setBuilding(Building* building);

    //void addFeatureByContext(PolygonFeature* polygon);
    PolygonFeature* createPolygonByContext();
    void deletePolygonByContext(PolygonFeature* feature);

    Floor* addFloor(Floor* floor = 0);
    Room* addRoom(Room* room);
    void addPubPoint(PubPoint* pubPoint);
    void setBackground(const QString & fileName);

    void deleteSelectedItems();
    void deleteSelectedLayers();
    void deleteMapFeature(Feature *feature);
    void removeMapFeature(Feature *feature);

    bool showFloor(int floorId);
    bool showDefaultFloor();
    Floor* currentFloor() const;
    void setCurrentFloor(Floor* floor);

    QList<Feature *> findMapFeature(const QString & name);
    void selectMapFeature(Feature* feature); //select the room and change the floor

    QList<QList<Feature*> > findAllRepeat();

    void transformMap(const QMatrix &matrix);
    void addScale(double s);
    void clearSelectedLayers();
    void setSelectedLayer(Feature *feature);
    Feature* currentLayer();
signals:
    void buildingChanged();
    void fontChanged(const QFont &font);
public slots:
    void convertSelectedToBuilding();
    void convertSelectedToFloor();
    void convertSelectedToRoom();
protected:
    void mousePressEvent( QGraphicsSceneMouseEvent *event );
    void mouseReleaseEvent( QGraphicsSceneMouseEvent *event );
    void mouseMoveEvent( QGraphicsSceneMouseEvent *event );
//    bool event(QEvent *event);
    //context menu
    void contextMenuEvent(QGraphicsSceneContextMenuEvent * event);
private:
//    Feature *m_root;
    ImageLayer *m_root;
    Floor *m_curFloor;
    double m_scaleSum;
    int m_scaleNum;
    double m_curScale;
    QList<Feature*> m_selectedLayers;
    QString bg_fileName;
};

#endif // SCENE_H
