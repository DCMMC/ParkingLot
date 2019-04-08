#ifndef POLYGONENTITY_H
#define POLYGONENTITY_H

#include "feature.h"
#include <QString>
#include <QJsonArray>
#include <QGraphicsObject>
#include <QPolygon>

class PolygonFeature : public Feature
{
    Q_OBJECT
public:
    explicit PolygonFeature(QGraphicsItem *parent = nullptr);
    explicit PolygonFeature(const QString & name, QGraphicsItem *parent = nullptr);
    PolygonFeature( const QString & name, int id);
    PolygonFeature( const QString & name, const QPolygon& poly);

    //copy the data from @polygon, used in subclasses
    void copy(PolygonFeature &polygon);
    //setters and getters
    QPolygon & outline();
    void setOutline(const QVector<QPoint> & points);
    double area();
    void setArea(double area);

    //add a point to tail
    void addPoint(const QPoint & p);

    //move the point at @id by @vector
    void movePoint(int id, const QPoint & vector);

    //move the point at @id to @point
    void movePointTo(int id, const QPoint & point);

    //insert a @point at @id
    void insertPoint(int id, const QPoint & p);

    //remove the point at @id
    void removePoint(int id);

    int PointNum() const;

    //set color
    void setColor(QColor color);

    //compute the center
    const QPointF & computeCenter();

    //compute the area
    double computeArea();

    //compute the OBB (oriented bounding box) main direction
    QPointF computeMainDir();

    //QGraphicsItem functions
    QRectF boundingRect() const override;
    QPainterPath shape() const override;
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;

    //io
    bool load(const QJsonObject & jsonObject) override;
    bool save(QJsonObject & jsonObject) const override;

    void transformFeature(const QMatrix &matrix) override;
protected:

    double m_frontAngle;

    QPolygon m_outline;
    QColor m_color;
    double m_area;
};

#endif // POLYGONENTITY_H
