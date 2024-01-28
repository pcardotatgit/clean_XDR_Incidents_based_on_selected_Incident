# clean XDR Incidents

These scripts help to completely clean up Incidents and every related objects that had been created around the incident.

When you run the script **1-select_incident_to_delete.py** , it first display the list of all Incidents that exist into your tenant.

Then you can select one of them thanks to an index.

Next the script create a lot of resulting files into the **./result** subfolder. Every **.txt** files contains object_IDs of every objects that are attached to the incident.

The next step is to run the **2-delete_selected_XDR_incident.py** script which reads the text files and delete one by one every objects they contain.

## Some explanation

When we create an **Incident** within XDR, we use to create other objects that are attached to this **incident**.

We create :

- **Incident**
- **Sightings** now called **events**
- **Judgments**
- **Relationships**

An incident contains one or several Sightings. Every sightings contains targets and malicious observables. Relationships are used to attach sightings to Incidents, they are used to attach Observables to targets and to attach observables in judgments to Indicators and feeds.

All the object that are attached to an Incident are linked together thanks to their IDs and relationships. This is actually a tree of IDs.

So we just have to start from the Selected Incident IDs and then we can rebuild the full relatinship tree. When doing that we keep every object IDs into resulting files, and the final operation is to use the Delete APIs and pass to it every Object ID one by one.

## How to do

### Step 1 : edit the config.txt file

And set the correct values for the variables.

### Step 2 : Run the script one after the other

    python 1-select_incident_to_delete.py
    python 2-delete_selected_XDR_incident.py