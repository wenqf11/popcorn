package cn.edu.tsinghua.thss.popcorn;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.beardedhen.androidbootstrap.FontAwesomeText;

public class RecordActivity extends ListActivity {

    private List<Map<String, Object>> mData;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String[] str_title = {"设备一","设备二","设备三","设备四","设备五"};
        mData = getData(str_title);
        AnimalListAdapter adapter = new AnimalListAdapter (this);
        setListAdapter(adapter);
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent=new Intent(this, TableActivity.class);
        Bundle bundle=new Bundle();
        intent.putExtras(bundle);
        //执行意图
        startActivity(intent);

        Log.v("MyListView4-click", (String) mData.get(position).get("title"));
        super.onListItemClick(l, v, position, id);
    }


    private List<Map<String, Object>> getData(String[] str_title) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_title.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("title", str_title[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView title;
        public FontAwesomeText faText;
    }

    public class AnimalListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public AnimalListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            return mData.size();
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.faText = (FontAwesomeText) convertView.findViewById(R.id.front_icon);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText((String)mData.get(position).get("title"));
           if(position == 1) {
               holder.faText.setTextColor(Color.parseColor("#D3D3D3"));
           }
           return convertView;
        }
    }
}