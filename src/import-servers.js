var imported_httpd_servers = findResources("Apache HTTP Server");

println("Imported Apache HTTPD servers:");
printServers(imported_httpd_servers);

println("Discovering new Apache HTTPD servers...");
var discovered_httpd_servers = findResources("Apache HTTP Server", false);

if (discovered_httpd_servers != null && discovered_httpd_servers.size() > 0) {
    println("Disovered " + discovered_httpd_servers.size() + " Apache HTTPD servers:");

    var httpdResourceIds = [];

    for (i = 0; i < discovered_httpd_servers.size(); i++) {
        var discovered_httpd_server = discovered_httpd_servers.get(i);

        addDependencyIds(discovered_httpd_server, httpdResourceIds);

        println(" - " + discovered_httpd_server.name);
        println("   Reconfiguring agent...");

        var address = discovered_httpd_server.name.match(new RegExp("^[\\w\\-]+", "g"))[0];
        var httpd = ProxyFactory.getResource(discovered_httpd_server.id);
        var httpd_configuration = httpd.getPluginConfiguration();

        httpd_configuration.getSimple("url").setStringValue("http://" + address);
        httpd.updatePluginConfiguration(httpd_configuration);

        println("   Agent reconfigured.");
    }

    println("Importing " + discovered_httpd_servers.size() + " Apache HTTPD servers...");
    DiscoveryBoss.importResources(httpdResourceIds);
    println("Imported.");

} else {
    println("No servers found.")
}

var imported_jboss_servers = findResources("JBossAS Server");

println("Imported JBoss AS 5/6 servers:");
printServers(imported_jboss_servers);

println("Discovering new JBoss AS 5/6 servers...");
var discovered_jboss_servers = findResources("JBossAS Server", false);
printServers(discovered_jboss_servers);

if (discovered_jboss_servers != null && discovered_jboss_servers.size() > 0) {
    var jbossResourceIds = [];

    for (i = 0; i < discovered_jboss_servers.size(); i++) {
        addDependencyIds(discovered_jboss_servers.get(i), jbossResourceIds);
    }

    println("Importing " + discovered_jboss_servers.size() + " JBoss AS 5/6 servers...");
    DiscoveryBoss.importResources(jbossResourceIds);
    println("Imported.");
}

function findResources(name, imported) {
    imported = typeof(imported) != 'undefined' ? imported : true;

    var criteria = new ResourceCriteria();

    criteria.addFilterResourceTypeName(name);

    if (!imported) {
        criteria.addFilterInventoryStatus(InventoryStatus.NEW);
    }

    return ResourceManager.findResourcesByCriteria(criteria);
}

function addDependencyIds(resource, array) {
    var parentResource = ResourceManager.getResource(resource.id).getParentResource();

    if (parentResource != null) {
        parentResource = ResourceManager.getResource(parentResource.id);

        if (parentResource.getInventoryStatus().equals(InventoryStatus.NEW))
            addDependencyIds(parentResource, array);
    }

    array.push(resource.id);
}

function printServers(resources) {
    if (resources != null && resources.size() > 0) {
        for (var i = 0; i < resources.size(); i++) {
            var resource = resources.get(i);
            println(" - " + resource.name);
        }
    } else {
        println("No servers found.")
    }
}
