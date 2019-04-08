#ifndef ROOM_H
#define ROOM_H

#include "polygonfeature.h"
#include <QHash>
#include <QString>
#include <QJsonObject>
#include <QGraphicsSceneMouseEvent>

class QGraphicsTextItem;

class Room : public PolygonFeature
{

    Q_OBJECT
public:
    // 车位状态
    enum AreaStatus{
        UNUSED = 0,   // 空车位
        USED = 1     // 正在使用中
    };

    // 实体类别
    enum SORT_TYPE
    {
        UNSORTED = 0,       // 未分类
        PARKING_LOT = 1,    // 车位
        // 墙体
        WALL = 2,
        // 入口
        IN_DOOR = 3,
        // 出口
        OUT_DOOR = 4,
    };

    //业态
//    enum Category{
//        None = 0,
//        Catering = 101,     //餐饮
//        Shopping = 102,     //购物
//        Beauty = 103,       //美妆丽人
//        ParentChild = 104,  //亲子儿童
//        LifeService = 105,  //生活服务
//        Education = 106,    //教育培训
//        LifeStyle = 107,    //生活方式
//        Entertainment = 108,//休闲娱乐
//        Other = 109         //其他
//    };

public:
    explicit Room(QGraphicsItem *parent = nullptr);
    explicit Room(PolygonFeature &polygon);
    Room( const QString & name, const QPolygon& poly);

    bool load(const QJsonObject & jsonObject) override;
    bool save(QJsonObject &jsonObject) const override;

//    QGraphicsTextItem *m_textItem; // 用于名称显示

    //setters and getters
    QString parkingNo() const;
    void setParkingNo(const QString &parkingNo);

//    Room::Category category() const;
//    void setCategory(Room::Category cate);

//    int dianpingId() const;
//    void setDianpingId(int dpId);

//    void setMateId(int id);
//    int mateId() const;

    void setAreaStatus(Room::AreaStatus areaStatus);
    Room::AreaStatus areaStatus() const;

    void setSortType(Room::SORT_TYPE sortType);
    Room::SORT_TYPE sortType();

//    const QStringList typeStringList() const;
//    virtual QString getTypeName();
//    virtual void updateByTypeName(const QString &name);

    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;
    void setTextItemVisible(bool visible);
    // m_textItem 的 visible, 默认 false
    bool text_visible;
protected:
    QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;
private slots:
    void updateName(const QString &name);
    void updateCenter(const QPointF &center);
    void updateFont(const QFont &font);
    void updateColor();
private:
    QString m_parkingNo;       // 车位号
//    Category m_category;    //业态
//    int m_brandShop;    //有品牌入驻的铺位id
//    int m_dianpingId;   //点评id，临时使用
    bool m_connected;   //slots have been connected
//    int m_mateId;       //同铺关联id
    static QHash<QString, int> m_typeHash;
    AreaStatus m_areaStatus;    // 实体状态
    SORT_TYPE m_sortType;       // 实体类型
    // 鼠标拖动
    bool m_dragValid = false;
    void mousePressEvent(QGraphicsSceneMouseEvent *event) override;
    void mouseMoveEvent(QGraphicsSceneMouseEvent *event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override;
};

#endif // ROOM_H
