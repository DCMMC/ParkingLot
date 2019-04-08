#include "propviewfloor.h"
#include "../core/floor.h"
#include "../core/room.h"
#include <QLineEdit>
#include <QLabel>
#include <QFormLayout>
#include <QDebug>

#pragma execution_character_set("utf-8")

PropViewFloor::PropViewFloor(Feature *mapFeature, QWidget *parent) :
    PropertyView(mapFeature, parent)
{
    m_heightEdit = new QLineEdit;
    m_funcAreaNumLabel = new QLabel;
    m_inDoorNumLabel = new QLabel;
    m_outDoorNumLabel = new QLabel;

    updateWidgets();

    m_layout->addRow(tr("高度"), m_heightEdit);
    m_layout->addRow(tr("车位数"), m_funcAreaNumLabel);
    m_layout->addRow(tr("入口数量"), m_inDoorNumLabel);
    m_layout->addRow(tr("出口数量"), m_outDoorNumLabel);

    connect(m_heightEdit, SIGNAL(textEdited(QString)), this, SLOT(updateHeight(QString)));
}

bool PropViewFloor::match(const Feature *mapFeature) const {
    return mapFeature->isClassOf("Floor");
}

void PropViewFloor::updateWidgets(){
    PropertyView::updateWidgets();
    auto floor = dynamic_cast<Floor*>(m_mapFeature);
    m_heightEdit->setText(QString::number(floor->height()));
    if (m_mapFeature->isClassOf("Floor")) {
        auto f = dynamic_cast<Floor *>(m_mapFeature);
        int lotCnt = 0, inCnt = 0, outCnt = 0;
        for (auto child : f->children()) {
            if (!QString(child->metaObject()->className()).compare("Room")) {
                switch (dynamic_cast<Room *>(child)->sortType()) {
                    case Room::PARKING_LOT:
                        lotCnt++;
                        break;
                    case Room::IN_DOOR:
                        inCnt++;
                        break;
                    case Room::OUT_DOOR:
                        outCnt++;
                        break;
                }
            }
        }
        m_funcAreaNumLabel->setText(QString::number(lotCnt));
        m_inDoorNumLabel->setText((QString::number(inCnt)));
        m_outDoorNumLabel->setText(QString::number(outCnt));
    }
}

void PropViewFloor::updateHeight(const QString &height) {
    dynamic_cast<Floor*>(m_mapFeature)->setHeight(height.toDouble());
}
