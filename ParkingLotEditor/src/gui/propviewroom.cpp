#include "propviewroom.h"


#include <QLineEdit>
#include <QHBoxLayout>
#include <QPushButton>
#include <QFormLayout>
#include <QComboBox>
#include <QCheckBox>

#pragma comment(lib,"Qt5Widgets.lib")
#pragma execution_character_set("utf-8")

PropViewRoom::PropViewRoom(Feature *mapFeature, QWidget *parent) :
    PropertyView(mapFeature, parent)
{
    m_room = dynamic_cast<Room*>(mapFeature);

    m_parkingNoEdit = new QLineEdit;
    m_areaEdit = new QLineEdit;
//    m_dianpingIdEdit = new QLineEdit;
//    m_queryButton = new QPushButton(tr("品牌关联"));
//    m_checkDianpingBtn = new QPushButton(tr("检查"));
//    m_mateIdEdit = new QLineEdit;
    m_sortComboBox = new QComboBox;
    QStringList strlist ;
    strlist<<"停车位"<< "墙体" << "入口" << "出口" << "无分类";
    m_sortComboBox->addItems(strlist);
    m_vacancyCheckBox = new QCheckBox;
    m_vacancyCheckBox->setText(tr("空车位"));
//    m_showName->setText(tr("显示名称"));

    // TODO: 自动分配车位号
    m_layout->addRow(tr("实体类别"), m_sortComboBox);
    m_layout->addRow(tr("<b><font color=red>车位号</font></b>"), m_parkingNoEdit);
    m_layout->addRow(tr("面积（平方米）"), m_areaEdit);
//    QHBoxLayout *dianpingLayout = new QHBoxLayout();
//    dianpingLayout->addWidget(m_dianpingIdEdit);
//    dianpingLayout->addWidget(m_checkDianpingBtn);
//    m_layout->addRow(tr("<b><font color=red>点评 ID</font></b>"), dianpingLayout);
//    m_layout->insertRow(0,m_queryButton);
//    m_layout->addRow(tr("同铺id"), m_mateIdEdit);
    m_layout->addRow(tr("车位状态"), m_vacancyCheckBox);

    updateWidgets();

    connect(m_parkingNoEdit, SIGNAL(textEdited(QString)), this, SLOT(updateParkingNo(QString)));
    connect(m_areaEdit, SIGNAL(textEdited(QString)), this, SLOT(updateArea(QString)));
//    connect(m_dianpingIdEdit, SIGNAL(textEdited(QString)), this, SLOT(updateDianpingId(QString)));
//    connect(m_queryButton, SIGNAL(clicked()), this, SLOT(onQuery()));
//    connect(m_mateIdEdit, SIGNAL(textEdited(QString)), this, SLOT(updateMateId(QString)) );
    connect(m_sortComboBox, SIGNAL(currentIndexChanged(QString)), this, SLOT(updateSortType(QString)));
    connect(m_vacancyCheckBox, SIGNAL(stateChanged(int)), this, SLOT(updateAreaStatus(int)));
}

PropViewRoom::~PropViewRoom() = default;

bool PropViewRoom::match(const Feature *mapFeature) const {
    return mapFeature->isClassOf("Room");
}

void PropViewRoom::updateWidgets(){
    PropertyView::updateWidgets();
    m_room = dynamic_cast<Room*>(m_mapFeature);

    m_parkingNoEdit->setText(m_room->parkingNo());
    m_areaEdit->setText(QString::number(m_room->area()));
//    m_dianpingIdEdit->setText(QString::number(m_room->dianpingId()));
//    m_mateIdEdit->setText(QString::number(m_room->mateId()));
    m_sortComboBox->setCurrentText(getSortTypeName(m_room->sortType()));
    m_vacancyCheckBox->setChecked(m_room->areaStatus() == Room::USED);
}

void PropViewRoom::updateParkingNo(const QString &parkingNo){
    m_room->setParkingNo(parkingNo);
}

void PropViewRoom::updateArea(const QString &area) {
    m_room->setArea(area.toDouble());
}

//void PropViewRoom::updateDianpingId(const QString &dpId) {
//    m_room->setDianpingId(dpId.toInt());
//}

//void PropViewRoom::updateMateId(const QString &mateId){
//    m_room->setMateId(mateId.toInt());
//}

void PropViewRoom::updateSortType(const QString &sortType){
    Room::SORT_TYPE type;
    if(!sortType.compare("停车位")){
        type = Room::PARKING_LOT;
    }else if(!sortType.compare("墙体")){
        type = Room::WALL;
    } else if (!sortType.compare("出口")) {
        type = Room::OUT_DOOR;
    } else if (!sortType.compare("入口")) {
        type = Room::IN_DOOR;
    } else {
        type = Room::UNSORTED;
    }
    m_room->setSortType(type);
}

void PropViewRoom::updateAreaStatus(const int state){
    if(state == Qt::Checked)
        m_room->setAreaStatus(Room::UNUSED);
    else if(state == Qt::Unchecked)
        m_room->setAreaStatus(Room::USED);
}

//void PropViewRoom::queryFinished(){
//    m_webDlg->close();
//    delete m_webDlg;
//    m_webDlg = NULL;
//}
//
//void PropViewRoom::onQuery(){
//
//}
//
//void PropViewRoom::addJsObject(){
//
//}


QString PropViewRoom::getSortTypeName(Room::SORT_TYPE sortType){
    if(sortType == Room::UNSORTED)
        return "无分类";
    if(sortType == Room::WALL)
        return "墙体";
    if(sortType == Room::PARKING_LOT)
        return "停车位";
    if (sortType == Room::IN_DOOR)
        return "入口";
    if (sortType == Room::OUT_DOOR)
        return "出口";
    return "未知";
}
