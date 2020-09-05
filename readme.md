[![HitCount](http://hits.dwyl.com/JavierOramas/PNServer.svg)](http://hits.dwyl.com/JavierOramas/PNServer)
# Prime Networks Comander Server

## What is PNCmdr?
<p>PNCmdr's purpose is to give easy access to all servers and services withon those servers in a flexible way, in order to allow you to painlesly consume, manage and enjoy your lLocal Network</p>

## Installation

In a terminal type:

<code>pip install -r requirements.txt</code>

## Technologies
<ul>
    <li>SQLite3</li>
    <li>Python3</br>
        <ul>
            <li>Flask 1.1.1</li>
            <li>Flask_SQLAchemy 2.4.4</li>
            <li>Requests 1.23.0</li>
            <li>Pandas o.25.1</li>
        </ul>
    </li>
    <li>Bootstrap 4.5</li>
</ul>

## Default Services
<ul>
    <li>
        <p>
            <b>PNCmdr</b>: Service Managing, only accessible for admins and superadmins of the server, Default Port: 2357
        <p>
    </li>
    <li>
        <p>
            <b>Emby</b>: Media Center Software, this will give you easy access to your all media from any device, it allows to get information about TV Shows, Movies and Music, also 
            can handle Home made photos and videos. For Better experience check their <a href='emby.org'>app</a>. Default Port: 8096
        <p>
    </li>
    <li>
        <p>
            <b>SMB</b>: Easyly Share files across your machines, add users with diferent access privilegies to keep privacy and security
        </p>
    </li>
    <li>
        <p>
            <b>FTP</b>: Easyly Share files across your machines, add users with diferent access privilegies to keep privacy and security. Default Port 20
        </p>
    </li>
    <li>
        <p>
            <b>Temp Monitor</b>: Useful tool to keep track of temperatures on your system, you can contribute to this app <a href='https://www.github.com/JavierOramas/ temp_monitor'>here</a></br>
            Also is available an api and an iphone and android app, you can use the mobile version for this <a href='https://www.github.com/JavierOramas/temp_monitor_app'>here</a>. </br>
            Default Ports: 9999 (server), 9998 (app)
        </p>
    </li>
</ul>

## Mobile Client
You can also use this system from your phone, Android or Iphone <a href='https://www.github.com/JavierOramas/PNCmdr'>here</a> this is a Work in progress so there might be some errors and stuff, all contributions are wellcome

## Desktop/Web
Our Mobile app is developed on Flutter, and soon many platforms such as web and linux Desktop will be supported, so... <a href='https://www.github.com/JavierOramas/PNCmdr'>stay close</a>. </br>
The Web Managing interface is running with the server on the port 2357

## Licence
MIT, you know, from the people, by the people and for the people
