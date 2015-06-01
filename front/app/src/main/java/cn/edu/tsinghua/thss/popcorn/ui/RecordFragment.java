package cn.edu.tsinghua.thss.popcorn.ui;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import android.content.Context;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import cn.edu.tsinghua.thss.popcorn.RecordListActivity;
import cn.edu.tsinghua.thss.popcorn.R;

/**
 * @author wenqingfu
 * @date 2015.04.12
 * @email thssvince@163.com
 */

public class RecordFragment extends ListFragment {
    private List<Map<String, Object>> mData;

	@Override
	public View onCreateView(LayoutInflater inflater,ViewGroup container,Bundle savedInstanceState){
		super.onCreateView(inflater, container, savedInstanceState);
		View recordView = inflater.inflate(R.layout.activity_tab_record, container,false);

        return recordView;
	}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        String[] str_title = {"线路一","线路二","线路三","线路四","线路五"};
        String[] str_time = {"8:00","10:00","12:00","14:00","16:00"};
        mData = getData(str_title, str_time);
        RouteListAdapter adapter = new RouteListAdapter (getActivity());
        setListAdapter(adapter);
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        Intent intent = new Intent(getActivity(), RecordListActivity.class);
        Bundle bundle = new Bundle();
        intent.putExtras(bundle);
        startActivity(intent);

        super.onListItemClick(l, v, position, id);
    }

    @Override
	public void onActivityCreated(Bundle savedInstanceState){
		super.onActivityCreated(savedInstanceState);
	}

    private List<Map<String, Object>> getData(String[] str_title, String[] str_time) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_title.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("title", str_title[i]);
            map.put("start_time", str_time[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView title;
        public TextView start_time;
    }

    public class RouteListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RouteListAdapter(Context context) {
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
                convertView = mInflater.inflate(R.layout.listview_tab_record, null);
                holder.title = (TextView) convertView.findViewById(R.id.title);
                holder.start_time = (TextView) convertView.findViewById(R.id.start_time);

                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.title.setText((String)mData.get(position).get("title"));
            holder.start_time.setText((String)mData.get(position).get("start_time"));

            return convertView;
        }
    }
}