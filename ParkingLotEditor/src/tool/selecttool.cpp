﻿#include "selecttool.h"
#include "../gui/documentview.h"
#include "../core/scene.h"
#include "../core/feature.h"
#include "../core/room.h"
#include <QMenu>
#include <QGraphicsSceneMouseEvent>
#include <QGraphicsSceneContextMenuEvent>
#include "../core/building.h"
#include <QDebug>

#pragma execution_character_set("utf-8")

SelectTool::SelectTool(DocumentView *doc) :
    AbstractTool(doc)
{
}

void SelectTool::contextMenuEvent(QGraphicsSceneContextMenuEvent *event) {
    Scene *scene = m_doc->scene();
    if(!scene->selectedItems().empty()){ //if sth selected
        auto feature = dynamic_cast<Feature*>(scene->selectedItems().at(0));
        if(feature != nullptr && feature->inherits("PolygonFeature")){ //if polygon feature selected
            if(m_contextMenu == nullptr){ //create the menu
                m_contextMenu = new QMenu();
                QAction *toBuildingAction = m_contextMenu->addAction("设为停车场");
                QAction *toFloorAction = m_contextMenu->addAction("设为楼层");
                QAction *toFuncAreaAction = m_contextMenu->addAction("设为实体");

                connect(toBuildingAction, SIGNAL(triggered()), scene, SLOT(convertSelectedToBuilding()));
                connect(toFloorAction, SIGNAL(triggered()), scene, SLOT(convertSelectedToFloor()));
                connect(toFuncAreaAction, SIGNAL(triggered()), scene, SLOT(convertSelectedToRoom()));
            }
            m_contextMenu->exec(event->screenPos());
        }
        event->accept();
    }
}
