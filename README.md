# scumBuster
Game community "Anti-Cheat" API created with Django, ReactJS, and PostgreSQL

## General Info
The tool's aim is to add an extra layer of security and "trustworthiness checks" before a player joins a community game server - whether it be on Counter Strike, Battlefield, Gary's Mod, or War Thunder, the API's main purpose is to filter out cheaters from our community. 

The "trustworthiness" of a player is based on the amount of reports a particular player has on their profile/id relative to the rest of the community. This data can be gathered from other public APIs, or even the scumBuster community!

## Mechanics  
For example, Player Foo, attempts to join a community server to play some Counter Strike! - let's call it "Community Server A". As Player Foo attempts to connect to the server, Community Server A, runs various custom made scripts to ensure Player Foo's experience is smooth i.e. Install extra assets, advertise the server's discord etc. 

However, one of these scripts, calls the scumBuster API to ensure that Player Foo is a trusthworthy player - he isn't a nusance and does not cheat. The API returns a JSON object that contains information relevant to their behaviour, and then it is up to the server owner on whether to accept Player Foo or not. 

The JSON Object may look something like this: 

```yaml
{
  'player_id': "Player Foo",
  'number_of_reports': 1234,
  'trust_factor': "untrustworthy",
}
```

## How is Data Gathered

As previously mentioned, data can be gathered via the Steam API and other game community DB's. Additionally, members of the gaming community will be able to send in their own report to cheaters and toxic players. Since 'trust_factor' is relative to the rest of the community - false reports should not have an impact on genuine players. 

## Running the Project (in it's current state)
Run this command from the root of the repository, once cloned.

```
pip install -r requirements.txt
```
